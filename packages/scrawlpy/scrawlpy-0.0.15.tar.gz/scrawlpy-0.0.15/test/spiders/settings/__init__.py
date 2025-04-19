# -*- coding: utf-8 -*-
# @Time   : 2024/5/1 01:27

import os

from attr import attrs, attrib, fields


@attrs
class Settings:
    # attr 对于不存在的变量会报错，所以这里定义一个 Extra 变量，用于存储额外的设置
    Extra = attrib(type=dict, default=None)
    # 使用 converter 参数将字符串转换为 float 类型,但如果通过属性赋值的话，是不会转换的
    Timeout = attrib(type=float, default=os.environ.get("Timeout", 3), converter=float)
    Name = attrib(type=str, default="scrawlpy")

    # MYNAME = attrib(type=str, default="scrawlpy")

    @classmethod
    def get_fields_map(cls):
        _fields = fields(cls)
        _fields_map = dict()
        for field in _fields:
            _fields_map[field.name] = field.type
        return _fields_map

    @classmethod
    def get_field_list(cls):
        _fields = fields(cls)
        fields_list = []
        for field in _fields:
            fields_list.append(field.name)
        return fields_list


class MyBaseSpider(object):
    __custom_setting__ = {
        "Timeout": "2.5",
        "KEEP_ALIVE": False,
    }
    Settings = Settings

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.settings = self.get_settings(kwargs.get("setting"))

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
        # 过滤掉Settings类中不存在的字段
        valid_settings = {key: value for key, value in combined_settings.items()
                          if key in self.Settings.get_field_list()}

        # 提取Settings类中不存在的额外设置, 因为 attr 里，如果未定义的变量传入会报错
        extra_settings = {key: value for key, value in combined_settings.items()
                          if key not in valid_settings}

        # 将有效的设置和额外设置传递给Settings类的构造函数
        settings = self.Settings(
            **valid_settings,
            Extra=extra_settings if extra_settings else None
        )
        return settings

    def run_spider(self):
        print(self.settings)


if __name__ == '__main__':
    _settings = {"setting": {"Command": "scrawlpy"}}
    spider = MyBaseSpider(**_settings)
    spider.run_spider()
