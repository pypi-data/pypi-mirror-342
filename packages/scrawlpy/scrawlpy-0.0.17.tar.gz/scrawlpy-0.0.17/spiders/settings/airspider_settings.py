# -*- coding: utf-8 -*-
# @Time   : 2024/5/1 01:27
import os

from scrawlpy.setting import BaseSettings
from attr import s, attrib


# @s
class SpiderSettings(BaseSettings):
    # Timeout = attrib(type=float, default=os.environ.get("Timeout", 3), converter=float)
    # TTimeout = attrib(type=float, default=os.environ.get("Timeout", 2), converter=float)
    # MYNAME = attrib(type=str, default="scrawlpy")
    Age = 33933.0
