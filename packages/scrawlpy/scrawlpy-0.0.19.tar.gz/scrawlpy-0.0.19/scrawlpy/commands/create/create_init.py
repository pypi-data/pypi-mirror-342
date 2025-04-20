# -*- coding: utf-8 -*-
"""
-*- coding: utf-8 -*-
@Time    : 2025/4/20 10:37
@Author  : jayden
"""


from scrawlpy.utils.tools import dumps_json

import feapder

class CreateInit:
    def create(self):
        __all__ = []

        import os

        path = os.getcwd()
        for file in os.listdir(path):
            if file.endswith(".py") and not file.startswith("__init__"):
                model = file.split(".")[0]
                __all__.append(model)

        del os

        with open("__init__.py", "w", encoding="utf-8") as file:
            text = "__all__ = %s" % dumps_json(__all__)
            file.write(text)
