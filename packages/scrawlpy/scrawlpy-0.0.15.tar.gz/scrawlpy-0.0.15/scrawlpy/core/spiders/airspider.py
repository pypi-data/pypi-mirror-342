# -*- coding: utf-8 -*-
# @Time   : 2024/4/30 17:16
import threading
import time

from scrawlpy.core.base_spider import AbstractSpider
from scrawlpy.storage.memorydb import MemoryDB
from scrawlpy.utils.concurrent_util import ThreadUtil

shutdown_event = threading.Event()
distribute_shutdown_event = threading.Event()


class AirSpider(AbstractSpider, ):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = kwargs
        self.max_worker = self.kwargs.get("max_worker", 1)
        self.crawler_threads = []
        self.request_queue = MemoryDB()

    def start_task_distribute(self) -> None:
        """
        分发任务
        Returns:

        """
        n = 0
        while not distribute_shutdown_event.is_set():
            self.request_queue.add({"url": "https://www.baidu.com"}, 1)
            self.request_queue.add({"url": "https://www.qq.com"}, 2)
            n += 2
            self.logger.info(f"当前任务数: {n}")
            time.sleep(0.1)
        self.logger.info(f"到超时时间了，任务分发结束...")

        # with ThreadPoolExecutor(max_workers=self.max_worker) as executor:
        #     executor.map(self._process_job, job_list)

    def _start_requests(self):

        seed = self.request_queue.get_nowait()
        while seed and not shutdown_event.is_set():
            self.start_requests(seed)
            seed = self.request_queue.get_nowait()
        # self.shutdown_event_queue.put(threading.get_ident())
        if not shutdown_event.is_set():
            shutdown_event.set()
            self.logger.info(f"{threading.get_ident()} 任务队列为空，发送退出信号..")
        else:
            self.logger.info(f"{threading.get_ident()} 接收退出信号，关闭spider线程.")
        # self.start_requests(seed)

    def start_requests(self, seed):
        print(seed)

    def shutdown_process(self, _shutdown_event, _process, timeout=5):
        """
        关闭进程，有两种方式
        1. 通过设置超时时间，超时时间到了之后关闭进程
        2. 通过接收到退出信号关闭进程，现在是收不到任务后，消费线程会发送退出信号
        Args:
            _shutdown_event: 退出信号
            _process:  处理线程
            timeout:

        Returns:

        """
        inter_val = 0.1
        has_sleep_time = 0
        while has_sleep_time <= timeout and not _shutdown_event.is_set():
            time.sleep(inter_val)
            has_sleep_time += 0.1
        if not _shutdown_event.is_set():
            _shutdown_event.set()
            is_receive_shutdown_signal = False
        else:
            is_receive_shutdown_signal = True
        _process.join()
        if is_receive_shutdown_signal:
            self.logger.info(f"{threading.get_ident()} {str(_process)} 已接收到退出信号，关闭当前线程...")
        else:
            self.logger.info(f"{threading.get_ident()} {str(_process)} 已到超时时间{timeout}，关闭当前线程...")

    def run_spider(self) -> None:
        """
        启动爬虫
        Returns:

        """
        _task_distribute = ThreadUtil.bg_run_task_on_thread(self.start_task_distribute, args=())
        shutdown_thread = threading.Thread(target=self.shutdown_process,
                                           args=(
                                               distribute_shutdown_event, _task_distribute, 4,))
        shutdown_thread.daemon = True
        shutdown_thread.start()

        # 创建定时关闭进程的线程
        for i in range(self.max_worker):
            spider_thread = threading.Thread(target=self._start_requests)
            spider_thread.start()

            # 创建定时关闭进程的线程
            shutdown_thread = threading.Thread(target=self.shutdown_process,
                                               args=(shutdown_event, spider_thread, self.settings.Timeout,))
            # shutdown_thread = threading.Thread(target=self.shutdown_process, args=(crawler_thread,self.settings.Timeout))
            # shutdown_thread.daemon = True
            shutdown_thread.start()


if __name__ == '__main__':
    spider = AirSpider(max_worker=2)
    spider.run_spider()
    # spider.start_task_distribute()
    # spider.run
