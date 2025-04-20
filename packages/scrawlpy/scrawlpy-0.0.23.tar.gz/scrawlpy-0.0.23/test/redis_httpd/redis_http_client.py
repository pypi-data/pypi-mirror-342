import requests
import datetime
import hmac
import hashlib
import base64
from typing import Any, Optional, List, Dict, Union
from functools import partial

from redis import Redis
from loguru import logger


class RedisHTTPError(Exception):
    """Redis HTTP客户端异常"""
    pass


class RedisHTTPClient(Redis):
    def __init__(self, base_url: str, username: str, password: str, source: str = "default", *args, **kwargs):
        """
        Redis HTTP 客户端

        :param base_url: 服务端基础URL，例如 "http://localhost:8000"
        :param username: 认证ID
        :param password: 认证密钥
        :param source: 请求来源标识(可选)
        """
        super().__init__(*args, **kwargs)  # 虽然不实际连接，但保持接口一致

        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.source = source
        self._session = requests.Session()

        # 封装请求方法
        self._get = partial(self._request, "GET")
        self._post = partial(self._request, "POST")

        try:
            self.register()
        except RedisHTTPError as e:
            logger.error(f"Redis HTTP Client registration failed: {str(e)}")
        # 初始化认证头
        self._update_auth_headers()

    def register(self, ) -> bool:
        """
        注册新客户端并获取凭证
        :param registration_code: 注册码(由服务端提供)
        :return: 是否注册成功
        """
        try:
            response = self._session.post(
                f"{self.base_url}/register",
                json={
                    "username": self.username,
                    "password": self.password,
                },
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            data = response.json()
            print(data)

            # if data.get("status") == "success":
            #     self.username = data["username"]
            #     self.password = data["password"]
            #     self._update_auth_headers()
            #     return True
            # return False
        except requests.exceptions.RequestException as e:
            raise RedisHTTPError(f"Registration failed: {str(e)}")

    def _generate_auth(self) -> tuple:
        """生成认证头和日期"""
        date_time = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        auth = 'hmac id="' + self.username + '", algorithm="hmac-sha1", headers="date source", signature="'
        sign_str = "date: " + date_time + "\n" + "source: " + self.source
        sign = hmac.new(self.password.encode(), sign_str.encode(), hashlib.sha1).digest()
        sign = base64.b64encode(sign).decode()
        return auth + sign + '"', date_time

    def _update_auth_headers(self):
        """更新认证头"""
        auth, date = self._generate_auth()
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth}',
            'Date': date,
            'Source': self.source,
            "Username": self.username,

        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送HTTP请求"""
        self._update_auth_headers()  # 每次请求前更新认证头
        url = f"{self.base_url}{endpoint}"

        try:
            response = self._session.request(
                method,
                url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json().get('detail', '')
                    error_msg += f", Detail: {error_detail}"
                except:
                    pass
            raise RedisHTTPError(error_msg)

    def execute_command(self, *args, **kwargs) -> Any:
        """执行Redis命令"""
        command = args[0]
        data = {
            "command": command,
            "args": args[1:],
            "kwargs": kwargs
        }
        response = self._post(
            "/api/redis/execute",
            json=data
        )
        return response.get("data")

    def create_bloom_filter(self, key: str, capacity: int = 10000, error_rate: float = 0.01) -> bool:
        """创建布隆过滤器"""
        response = self._post(
            "/api/redis/bloom/create",
            json={
                "key": key,
                "capacity": capacity,
                "error_rate": error_rate
            }
        )
        return response.get("status") == "success"

    def bloom_add(self, key: str, *items: str) -> Union[bool, List[bool]]:
        """向布隆过滤器添加元素"""
        response = self._post(
            "/api/redis/bloom/add",
            json={
                "key": key,
                "items": items if len(items) > 1 else [items[0]] if items else []
            }
        )
        result = response.get("data")
        return result[0] if len(items) == 1 else result

    def bloom_check(self, key: str, *items: str) -> Union[bool, List[bool]]:
        """检查元素是否在布隆过滤器中"""
        response = self._post(
            "/api/redis/bloom/check",
            json={
                "key": key,
                "items": items if len(items) > 1 else [items[0]] if items else []
            }
        )
        result = response.get("data")
        return result[0] if len(items) == 1 else result

    def get_memory_info(self) -> Dict[str, Any]:
        """获取内存信息"""
        return self._get("/api/redis/monitor/memory").get("data")

    def get_slow_queries(self) -> List[Dict[str, Any]]:
        """获取慢查询日志"""
        return self._get("/api/redis/monitor/slow_queries").get("data")


if __name__ == '__main__':
    # 初始化客户端
    client = RedisHTTPClient(
        base_url="http://localhost:8081",
        username="jayden",
        password="jayden",
        source="text2image"  # 可选，标识请求来源
    )

    # 1. 基本键值操作
    client.set("user:wu", "de")
    result = client.get("user:wu")
    print(result)
    # client.set("user:1001", json.dumps({"name": "Alice", "age": 30}), ex=3600)
    # user_data = json.loads(client.get("user:1001"))
    # print(f"User data: {user_data}")

    # # 2. 布隆过滤器操作
    # client.create_bloom_filter("visited_urls", capacity=100000, error_rate=0.001)
    # client.bloom_add("visited_urls", "https://example.com/page1")
    # if client.bloom_check("visited_urls", "https://example.com/page1"):
    #     print("URL already visited")
    #
    # # 3. 监控信息
    memory_info = client.get_memory_info()
    print(f"Memory usage: {memory_info['used_memory'] / 1024 / 1024:.2f} MB")
    #
    # # 4. 兼容Redis原生API的用法
    keys = client.keys("user:*")
    print(f"Found keys: {keys}")

    # 5. 错误处理
    # try:
    #     client.execute_command("NON_EXISTENT_COMMAND")
    # except RedisHTTPError as e:
    #     print(f"Error executing command: {str(e)}")
