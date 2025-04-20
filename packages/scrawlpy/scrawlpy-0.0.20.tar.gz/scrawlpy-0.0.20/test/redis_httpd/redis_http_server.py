import os
import sqlite3
import datetime
import hmac
import hashlib
import base64
import time
import traceback
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Depends, HTTPException, Header, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import redis
import math
from collections import deque

"""
pip3 install fastapi uvicorn redis passlib python-jose[cryptography] slowapi
"""
# 初始化
app = FastAPI(title="Redis HTTP Proxy", version="1.0.0")
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger(__name__)


# 配置
class Config:
    SQLITE_DB_PATH = "users.db"
    TOKEN_EXPIRE_MINUTES = 30  # Token有效期30分钟
    RATE_LIMIT = "50/minute"
    MEMORY_LIMIT = 1024 * 1024 * 1024 * 2  # 2GB内存限制
    SLOW_QUERY_THRESHOLD = 100  # 100ms视为慢查询
    DEFAULT_BLOOM_ERROR_RATE = 0.01
    DEFAULT_BLOOM_CAPACITY = 10000


# Redis连接
redis_client = redis.StrictRedis(
    host="localhost",
    port=6379,
    password="",
    decode_responses=False
)

# 全局状态
slow_queries = deque(maxlen=1000)  # 慢查询日志


# 数据库模型
class UserCreate(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime.datetime
    last_login: Optional[datetime.datetime]


class TokenInfo(BaseModel):
    token: str
    expires_at: datetime.datetime


# 数据库初始化
def init_db():
    if not os.path.exists(Config.SQLITE_DB_PATH):
        conn = sqlite3.connect(Config.SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()


init_db()


# 数据库访问层
class UserDB:
    @staticmethod
    def get_user(username: str) -> Optional[UserInDB]:
        conn = sqlite3.connect(Config.SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return UserInDB(**dict(row))
        return None

    @staticmethod
    def create_user(user: UserCreate) -> UserInDB:
        conn = sqlite3.connect(Config.SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO users 
            (username, password) 
            VALUES (?, ?)""",
            (user.username, user.password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return UserDB.get_user(user.username)

    @staticmethod
    def update_last_login(username: str):
        conn = sqlite3.connect(Config.SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET last_login=CURRENT_TIMESTAMP WHERE username=?",
            (username,)
        )
        conn.commit()
        conn.close()


# 认证工具
def get_simple_auth(source: str, username: str, password: str) -> tuple:
    """生成认证头和日期"""
    date_time = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    auth = 'hmac id="' + username + '", algorithm="hmac-sha1", headers="date source", signature="'
    sign_str = "date: " + date_time + "\n" + "source: " + source
    sign = hmac.new(password.encode(), sign_str.encode(), hashlib.sha1).digest()
    sign = base64.b64encode(sign).decode()
    return auth + sign + '"', date_time


def verify_auth(
        auth: str,
        date: str,
        username: str,
        source: str,
        check_expiry: bool = True
) -> bool:
    """验证认证信息"""
    try:
        # 检查时间是否过期
        if check_expiry:
            request_time = datetime.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S GMT")
            expiry_time = request_time + datetime.timedelta(minutes=Config.TOKEN_EXPIRE_MINUTES)
            if datetime.datetime.utcnow() > expiry_time:
                return False

        # 解析auth头
        parts = auth.split('"')
        signature = parts[7]

        user = UserDB.get_user(username)
        if not user:
            return False

        # 重新计算签名
        sign_str = "date: " + date + "\n" + "source: " + source
        expected_sign = hmac.new(
            user.password.encode(),
            sign_str.encode(),
            hashlib.sha1
        ).digest()
        expected_sign = base64.b64encode(expected_sign).decode()

        return signature == expected_sign
    except Exception as e:
        logger.error(f"Auth verification failed: {str(e)}")
        return False


# Redis工具函数
def get_memory_info() -> int:
    """获取当前内存使用量"""
    return redis_client.info('memory')['used_memory']


def estimate_bloom_memory(capacity: int, error_rate: float) -> int:
    """估算布隆过滤器内存使用"""
    n = capacity
    p = error_rate
    bits_per_item = - (math.log(p) / (math.log(2) ** 2))
    bits = int(n * bits_per_item)
    return max(1, bits // 8)


def log_slow_query(command: str, execution_time: float, args: list = None):
    """记录慢查询"""
    slow_queries.append({
        'command': command,
        'time_ms': execution_time,
        'timestamp': datetime.datetime.now().isoformat(),
        'args': args or []
    })


# 认证依赖
async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        date: str = Header(...),
        source: str = Header(...),
        username: str = Header(...),
) -> UserInDB:
    """获取当前认证用户"""
    auth = credentials.credentials
    if not verify_auth(auth, date, username, source):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserDB.get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # 更新最后登录时间
    UserDB.update_last_login(user.username)
    return user


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理422验证错误"""
    error_details = []
    for error in exc.errors():
        error_details.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })

    logger.error(
        f"422 Validation Error\n"
        f"URL: {request.url}\n"
        f"Errors: {error_details}\n"
        f"Request body: {await request.body()}\n"
        f"Stack trace: {traceback.format_exc()}"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Validation error",
            "details": error_details
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """处理所有其他异常"""
    logger.error(
        f"Unhandled Exception\n"
        f"URL: {request.url}\n"
        f"Error: {str(exc)}\n"
        f"Type: {type(exc).__name__}\n"
        f"Stack trace: {traceback.format_exc()}\n"
        f"Request body: {await request.body()}"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc)
        },
    )


# 异常处理
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# 用户管理路由
@app.post("/register")
@limiter.limit("10/hour")
async def register(user: UserCreate, request: Request):
    """用户注册接口"""
    if UserDB.get_user(user.username):
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Username already exists"
        )

    # 创建用户 (密码未哈希处理，实际生产环境应该加盐哈希)
    created_user = UserDB.create_user(user)
    return {
        "status": "success",
        "message": "User registered successfully",
        "username": created_user.username
    }


@app.post("/login")
@limiter.limit("10/minute")
async def login(user: UserCreate, request: Request):
    """用户登录接口"""
    db_user = UserDB.get_user(user.username)
    if not db_user or db_user.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # 生成认证信息
    auth, date = get_simple_auth(
        db_user.username,
        db_user.password
    )

    # 更新最后登录时间
    UserDB.update_last_login(db_user.username)

    return {
        "status": "success",
        "auth": auth,
        "date": date,
        "username": db_user.username,
        "expires_in": Config.TOKEN_EXPIRE_MINUTES * 60
    }


# Redis服务路由
@app.post("/api/redis/execute")
@limiter.limit(Config.RATE_LIMIT)
async def execute_redis_command(
        request: Request,
        command_request: Dict[str, Any],
        current_user: UserInDB = Depends(get_current_user)
):
    """执行Redis命令"""
    start_time = time.time()
    try:
        command = command_request["command"].upper()
        args = command_request.get("args", [])
        kwargs = command_request.get("kwargs", {})

        # 执行命令
        result = redis_client.execute_command(command, *args, **kwargs)
        execution_time = (time.time() - start_time) * 1000

        # 记录慢查询
        if execution_time > Config.SLOW_QUERY_THRESHOLD:
            log_slow_query(command, execution_time, args)

        # 处理二进制返回
        if isinstance(result, bytes):
            result = result.decode('utf-8', errors='replace')

        return {
            "status": "success",
            "data": result,
            "execution_time": execution_time
        }
    except Exception as e:
        logger.error(f"Redis command failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/api/redis/bloom/create")
@limiter.limit(Config.RATE_LIMIT)
async def create_bloom_filter(
        request: Request,
        bloom_request: Dict[str, Any],
        current_user: UserInDB = Depends(get_current_user)
):
    """创建布隆过滤器"""
    try:
        key = bloom_request["key"]
        capacity = bloom_request.get("capacity", Config.DEFAULT_BLOOM_CAPACITY)
        error_rate = bloom_request.get("error_rate", Config.DEFAULT_BLOOM_ERROR_RATE)

        # 估算内存需求
        bytes_needed = estimate_bloom_memory(capacity, error_rate)
        used_memory = get_memory_info()

        if used_memory + bytes_needed > Config.MEMORY_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Not enough memory. Required: {bytes_needed}, Used: {used_memory}, Limit: {Config.MEMORY_LIMIT}"
            )

        # 创建布隆过滤器
        result = redis_client.execute_command(
            'BF.RESERVE',
            key,
            error_rate,
            capacity
        )

        return {
            "status": "success",
            "data": result,
            "estimated_memory": bytes_needed
        }
    except Exception as e:
        logger.error(f"Bloom create failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/api/redis/bloom/add")
@limiter.limit(Config.RATE_LIMIT)
async def bloom_add(
        request: Request,
        bloom_request: Dict[str, Any],
        current_user: UserInDB = Depends(get_current_user)
):
    """向布隆过滤器添加元素"""
    try:
        key = bloom_request["key"]
        items = bloom_request["items"]
        if not isinstance(items, list):
            items = [items]

        command = ['BF.ADD', key] if len(items) == 1 else ['BF.MADD', key]
        command.extend(items)

        start_time = time.time()
        result = redis_client.execute_command(*command)
        execution_time = (time.time() - start_time) * 1000

        if execution_time > Config.SLOW_QUERY_THRESHOLD:
            log_slow_query(
                'BF.ADD' if len(items) == 1 else 'BF.MADD',
                execution_time,
                {'key': key, 'item_count': len(items)}
            )

        return {
            "status": "success",
            "data": result,
            "execution_time": execution_time
        }
    except Exception as e:
        logger.error(f"Bloom add failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/api/redis/bloom/check")
@limiter.limit(Config.RATE_LIMIT)
async def bloom_check(
        request: Request,
        bloom_request: Dict[str, Any],
        current_user: UserInDB = Depends(get_current_user)
):
    """检查布隆过滤器元素"""
    try:
        key = bloom_request["key"]
        items = bloom_request["items"]
        if not isinstance(items, list):
            items = [items]

        command = ['BF.EXISTS', key] if len(items) == 1 else ['BF.MEXISTS', key]
        command.extend(items)

        start_time = time.time()
        result = redis_client.execute_command(*command)
        execution_time = (time.time() - start_time) * 1000

        if execution_time > Config.SLOW_QUERY_THRESHOLD:
            log_slow_query(
                'BF.EXISTS' if len(items) == 1 else 'BF.MEXISTS',
                execution_time,
                {'key': key, 'item_count': len(items)}
            )

        return {
            "status": "success",
            "data": result,
            "execution_time": execution_time
        }
    except Exception as e:
        logger.error(f"Bloom check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# 监控路由
@app.get("/api/redis/monitor/memory")
@limiter.limit("10/minute")
async def get_memory_info(
        request: Request,
        current_user: UserInDB = Depends(get_current_user)
):
    """获取内存信息"""
    try:
        info = redis_client.info('memory')
        return {
            "status": "success",
            "data": {
                "used_memory": info['used_memory'],
                "maxmemory": info['maxmemory'],
                "fragmentation_ratio": info['mem_fragmentation_ratio'],
                "limit": Config.MEMORY_LIMIT,
                "usage_percent": info['used_memory'] / Config.MEMORY_LIMIT * 100
            }
        }
    except Exception as e:
        logger.error(f"Memory info failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/api/redis/monitor/slow_queries")
@limiter.limit("10/minute")
async def get_slow_queries(
        request: Request,
        current_user: UserInDB = Depends(get_current_user)
):
    """获取慢查询日志"""
    return {
        "status": "success",
        "data": list(slow_queries)
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
