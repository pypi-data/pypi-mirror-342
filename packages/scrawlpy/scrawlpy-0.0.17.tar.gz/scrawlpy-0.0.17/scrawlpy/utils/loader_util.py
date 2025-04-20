# -*- coding: utf-8 -*-
# @Time   : 2020/10/23 17:47
# @Author : wu


from collections import defaultdict
from importlib import import_module
import inspect
import os
from os.path import abspath
from os.path import dirname
from os.path import join
from pkgutil import iter_modules
from pprint import pprint

import six

# from utils.log_util import get_logger

logger = get_logger(__name__)


class ModuleLoader(object):
    def __init__(self, module: str, base_class: object, sub_dir: str = None, module_path: str = None):
        """
        导入对应 app 下的所有模块，这些模块中的类必须都继承同一个基类
        Args:
            module: app，例如 dataparser
            base_class: 基类，例如 dataparser/__init__ 下的 BaseParser
            sub_dir: app 下的子目录，例如 dataparser 下的 kuaishou，在这里就只需要传入 kuaishou
            module_path: 模块的路径，传入此参数，表示导入模块下所有子目录下的类，例如 xxx/ym-crawler-ccs/dataparser
                         可使用 os.path.join(os.path.dirname(__file__), 'dataparsr')) 此类方式
            注意：如果同时传入 sub_dir 和 module_path，默认导入的是 module_path 下的所有类，两者必须传入一个
        """
        if not any([sub_dir, module_path]):
            raise TypeError("必须传入 sub_dir 或者 module_path 其中一个参数")
        self.module = module
        self.base_class = base_class
        self.sub_dir = sub_dir
        self.module_path = module_path
        self.modules = dict()
        self._found = defaultdict(list)

    def load_modules(self):

        app_modules = self._load_modules() if self.module_path else [f"{self.module}.{self.sub_dir}"]
        for sub_dir in app_modules:
            for module in self.walk_modules(sub_dir):
                self._load_spiders(module)
        self._check_name_duplicates()
        return self.modules

    def _load_modules(self):
        """
        自动加载 app 下的所有模块
        """
        _ignore_list = ["__pycache__", ".DS_Store"]
        # 获取ym-crawl-ccs项目绝对路径
        project_dir = dirname(dirname(abspath(__file__)))
        # 遍历指定模块下的目录或文件
        paths = []
        module_path = self.module_path or join(project_dir, self.module)
        _, dirs, _ = next(os.walk(module_path))
        for i in dirs:
            if i in _ignore_list:
                continue
            path = f"{self.module}.{i}"
            paths.append(path)
        return paths

    def walk_modules(self, path):
        """Loads a module and all its submodules from the given module path and
        returns them. If *any* module throws an exception while importing, that
        exception is thrown back.

        For example: walk_modules('dataparser.kuaishou')
        """

        mods = []
        mod = import_module(path)
        mods.append(mod)
        if hasattr(mod, "__path__"):
            for _, subpath, ispkg in iter_modules(mod.__path__):
                fullpath = path + "." + subpath
                if ispkg:
                    mods += self.walk_modules(fullpath)
                else:
                    submod = import_module(fullpath)
                    mods.append(submod)
        return mods

    def _load_spiders(self, module):
        for spcls in self.iter_spider_classes(module, self.base_class):
            self._found[spcls.name].append((module.__name__, spcls.__name__))
            self.modules[spcls.name] = spcls

    @staticmethod
    def iter_spider_classes(module, base_class):
        """Return an iterator over all spider classes defined in the given module
        that can be instantiated (ie. which have name)
        """

        for obj in six.itervalues(vars(module)):
            if (
                inspect.isclass(obj)
                and issubclass(obj, base_class)
                and obj.__module__ == module.__name__
                and getattr(obj, "name", None)
            ):
                yield obj

    def _check_name_duplicates(self):
        dupes = []
        for name, locations in self._found.items():
            dupes.extend(
                [
                    "  {cls} named {name!r} (in {module})".format(module=mod, cls=cls, name=name)
                    for mod, cls in locations
                    if len(locations) > 1
                ]
            )

        if dupes:
            dupes_string = "\n\n".join(dupes)
            raise NameError(
                "There are several modules with the same name:\n\n"
                "{}\n\n  This can cause unexpected behavior.".format(dupes_string),
                # category=UserWarning,
            )

    def load(self, name):
        """
        Return the app class for the given cls name. If the Class
        name is not found, raise a KeyError.
        """
        try:
            return self.modules[name]
        except KeyError:
            raise KeyError("Name not found: {}".format(name))

    def list(self):
        """
        Return a list with the names of all modules available in the project.
        """
        return list(self.modules.keys())


if __name__ == "__main__":
    from dataparser import BaseParser

    _module = "dataparser"
    _module_path = join(dirname(dirname(__file__)), _module)
    pprint(_module_path)
    modules = ModuleLoader(_module, BaseParser, module_path=_module_path).load_modules()
    pprint(modules)
