# -*- coding: utf-8 -*-
# @Time   : 2024/4/28 16:36

from scrawlpy.core.base_spider import AbstractSpider


class Spider(AbstractSpider):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def run(self):
        pass
