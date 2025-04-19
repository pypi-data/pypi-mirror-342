# -*- coding: utf-8 -*-
# @Time   : 2024/4/28 16:55
import threading

import scrawlpy
from scrawlpy import Request

from test.spiders.settings.airspider_settings import SpiderSettings


class Myspider(scrawlpy.AirSpider):
    Settings = SpiderSettings
    __custom_setting__ = {
        "Timeout": "5",
        "KEEP_ALIVE": False,
    }

    # def start_task_distribute(self) -> None:
    #     """
    #     分发任务
    #     Returns:
    #
    #     """
    #     while True:
    #         self.request_queue.add({"url": "https://www.baidu.com"}, 1)
    #         # self.request_queue.add({"url": "https://www.qq.com"}, 2)

    def start_requests(self, seed):
        # print(seed)
        priority, seed = seed
        # self.log.info()
        url = seed.get("url")
        self.logger.info(f"线程id: {threading.get_ident()} 超时时间: {self.settings.Timeout}")
        res = self.requests.get(url)
        # self.logger.info(res.text)
        # for i in range(10):
        #     yield Request("http://www.baidu.com", callback=self.parse)
        # res = self.requests.get("http://www.baidu.com")
        # print(res.text)


if __name__ == '__main__':
    settings = {"settings": {"Author": "Jayden"}}
    Myspider(max_worker=10, **settings).run_spider()
