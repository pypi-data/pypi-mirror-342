# -*- coding: utf-8 -*-
# @Time   : 2024/5/1 01:22
import inspect


def inspect_all_attr(obj):
    """修正基本类型转换"""
    attr_dict = {}

    for i in dir(obj):
        if str(i).startswith("__") or (not hasattr(obj, i)) or (i in ["args", "with_traceback"]):
            continue
        attr = getattr(obj, i)
        if inspect.ismethod(attr):
            continue

        flag = True
        for value_type in (list, dict, int, float, bool, str) or attr is None:
            if isinstance(attr, value_type):
                attr_dict[i] = attr
                flag = False
                break

        if flag:  # 非基本类型, 统一转字符串
            attr_dict[i] = str(attr)

    return attr_dict
