# -*- coding: utf-8 -*-
# @Time   : 2024/4/28 16:19
# -*- coding: utf-8 -*-
"""
Created on 2020/4/21 10:41 PM
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""
import os
import re
import sys

sys.path.insert(0, re.sub(r"([\\/]items$)|([\\/]spiders$)", "", os.getcwd()))

__all__ = [
    "AirSpider",
    "Spider",
    "BaseParser",
    "TaskParser",
    "BatchParser",
    "Request",
    "Response",
    "Item",
    "UpdateItem",
    "ArgumentParser",
]

from scrawlpy.core.spiders import AirSpider, Spider
from scrawlpy.core.base_parser import BaseParser, TaskParser, BatchParser
from scrawlpy.network.request import Request
from scrawlpy.network.response import Response
from scrawlpy.network.item import Item, UpdateItem
from scrawlpy.utils.custom_argparse import ArgumentParser

from scrawlpy.core.spiders import Spider
from scrawlpy.core.spiders import AirSpider
from scrawlpy.network.request import Request