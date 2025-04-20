# -*- coding: utf-8 -*-
# @Time   : 2024/4/30 18:52

import threading
import time
import queue
import sys

# 请求队列
request_queue = queue.Queue()

# 服务关闭标志
shutdown_flag = False

# 请求处理线程
request_handler_thread = None

def request_handler():
    global shutdown_flag
    while not shutdown_flag or not request_queue.empty():
        try:
            # 从队列中获取请求
            request = request_queue.get(timeout=5)  # 5秒超时
            # 模拟处理请求
            print(f"Handling request: {request}")
            time.sleep(1)  # 模拟请求处理时间
        except queue.Empty:
            if shutdown_flag:
                break
            continue
        finally:
        #     任务完成，通知队列
            request_queue.task_done()

    # 请求处理完毕或服务关闭标志被设置
    print("Request handler is stopping.")

def shutdown_service():
    global shutdown_flag, request_handler_thread
    print("Initiating shutdown sequence...")
    # 设置服务关闭标志
    shutdown_flag = True
    # 等待请求处理完成
    print("哈哈哈哈哈哈哈")
    # request_queue.join()
    print("嘻嘻嘻嘻嘻i")
    # 等待请求处理线程结束
    # request_handler_thread.join()
    print("All requests have been processed.")
    # 关闭其他资源（如网络连接、文件句柄等）
    # ...
    # 退出程序
    raise EOFError
    sys.exit(9)

def service():
    global request_handler_thread

    # 启动请求处理线程
    request_handler_thread = threading.Thread(target=request_handler, daemon=True)
    request_handler_thread.start()

    # 运行30分钟
    time.sleep(5)
    print("到点了，准备关闭服务...")

    # 调用关闭服务的函数
    shutdown_service()

# 模拟添加请求到队列
def add_request():
    request_queue.put("New request")

# 启动服务
service_thread = threading.Thread(target=service)
service_thread.start()

# 在这里可以模拟添加请求
# time.sleep(10)  # 等待一段时间
while True:
    add_request()  # 添加请求到队列
    time.sleep(0.1)
