import time
# import redis
import threading
from multiprocessing import Process, Event

# Redis连接配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
SEEDS_KEY = 'seeds'
from loguru import logger

# 全局事件，用于控制进程关闭
shutdown_event = Event()


class ShutdownDemo:

    def crawler_thread(self):
        while not shutdown_event.is_set():
            logger.info(f"{threading.get_ident()} Crawling...")
            # 在这里执行具体的爬取逻辑
            time.sleep(3)

    @staticmethod
    def shutdown_process(crawler_process):
        logger.info("Shutting down process in 3 minutes...")
        time.sleep(5)  # 在关闭之前等待3分钟
        logger.info(f"{threading.get_ident()} 到点啦")
        shutdown_event.set()
        crawler_process.join()

    def main(self):
        # 创建爬虫进程
        # crawler_process = Process(target=fetch_seed_from_redis)
        # crawler_process.start()

        # 创建爬虫线程
        for i in range(5):
            _crawler_thread = threading.Thread(target=self.crawler_thread)
            _crawler_thread.start()

            # 创建定时关闭进程的线程
            shutdown_thread = threading.Thread(target=self.shutdown_process, args=(_crawler_thread,))
            shutdown_thread.start()

            # shutdown_thread.join()

        logger.info("Main process has exited.")


if __name__ == "__main__":
    # main()
    ShutdownDemo().main()
