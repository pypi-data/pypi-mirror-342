# -*- coding: utf-8 -*-
# @Time   : 2024/4/30 19:01
import multiprocessing
import os
import time
import queue
import threading


def worker(q):
    while True:
        item = q.get()  # 从队列中获取任务
        if item is None:
            break  # 如果获取到None，表示没有更多任务
        print(f"Working on {item}")
        time.sleep(1)  # 模拟工作


def thread_target(q):
    # 创建工作线程
    threads = [threading.Thread(target=worker, args=(q,)) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()  # 等待所有线程完成


def main_process(q, timeout):
    # 模拟主进程的工作
    try:
        thread = threading.Thread(target=thread_target, args=(q,))
        thread.start()
        thread.join(timeout=timeout)  # 设置超时时间
    except threading.TimeoutError:
        print(f"Timed out after {timeout} seconds")
        # 如果超时，终止程序
        for i in range(os.cpu_count()):  # 向每个CPU发送终止信号
            os.kill(os.getpid(), 9)  # SIGKILL信号立即终止进程
    else:
        print("Main process completed successfully")


if __name__ == "__main__":
    # 创建任务队列
    q = queue.Queue()
    for i in range(10):
        q.put(i)

    # 设置超时时间（例如10秒）
    timeout = 10

    # 使用多进程创建定时器
    timer = multiprocessing.Process(target=main_process, args=(q, timeout))
    timer.start()
    timer.join()  # 等待定时器进程结束