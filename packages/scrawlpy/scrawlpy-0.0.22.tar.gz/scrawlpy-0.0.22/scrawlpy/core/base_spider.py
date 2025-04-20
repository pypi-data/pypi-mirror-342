# -*- coding: utf-8 -*-
# @Time   : 2024/4/28 16:29
import uuid
from abc import ABCMeta, abstractmethod


import requests
from urllib3.exceptions import InsecureRequestWarning

from scrawlpy.network.request import Request
from scrawlpy.utils.logger_util import get_bind_logger
from scrawlpy.setting import BaseSettings

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class AbstractSpider(metaclass=ABCMeta):
    project_name = "abstract_project"  # 项目
    spider_name = "abstract_spider"  # spider 接口
    site = "abstract"  # 站点
    Request = Request
    __custom_setting__ = dict()
    Settings = BaseSettings

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.spider_config = None
        self.logger = get_bind_logger(self.spider_name)
        self.requests = None
        self.is_daemon = False
        self.requests: Request = Request()
        self.settings = self.get_settings(kwargs.get("settings"))
        self.settings_dict = self.settings.fields_map()
        # self.settings_extra = self.settings.Extra

        self.logger.debug(self.settings)

    def get_settings(self, cmd_settings) -> Settings:
        """
        获取设置
        Args:
            cmd_settings:

        Returns:

        """

        if not cmd_settings:
            cmd_settings = dict()
        # 合并自定义设置和命令行设置，命令行设置优先级更高
        combined_settings = {**self.__custom_setting__, **cmd_settings}

        # 将有效的设置和额外设置传递给Settings类的构造函数
        for k, v in combined_settings.items():
            # 判断是否存在该属性，如果存在则需要根据类型进行转换，否则直接赋值
            if hasattr(self.Settings, k):
                setattr(self.Settings, k, self.Settings.convert_type(self.Settings.fields_map_type()[k], v))
            else:
                setattr(self.Settings, k, v)

        return self.Settings()

    # def start_requests(self):
    #     pass

    def parse(self, response, **kwargs):
        pass
