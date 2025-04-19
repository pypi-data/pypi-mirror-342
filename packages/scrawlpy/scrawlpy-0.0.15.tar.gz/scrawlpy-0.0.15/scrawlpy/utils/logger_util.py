# -*- coding: utf-8 -*-
# @Time   : 2024/5/1 00:46
import os
import sys

from loguru import logger

logger_cache = dict()

l_class = logger.__class__


def get_bind_logger(name, base_dir="", log_format=None, log_level="DEBUG") -> l_class:
    if name in logger_cache:
        return logger_cache.get(name)
    # if not base_dir:
    #     base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "default_logger")
    # log_file_path = os.path.join(base_dir, f'{name}_{os.getgid()}')
    # logger.add(log_file_path + '.log', level="DEBUG", filter=make_filter(name), colorize=False,
    #            rotation='100 MB', retention='30 days', encoding='utf-8')
    #
    logger.remove()
    logger.add(sink=sys.stderr, level=log_level, )
    logger_cache[name] = logger.bind(name=name)
    return logger_cache.get(name)
