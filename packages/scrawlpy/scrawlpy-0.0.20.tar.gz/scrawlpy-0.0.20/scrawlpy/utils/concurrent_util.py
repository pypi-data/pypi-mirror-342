# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/20 10:37
@Author  : jayden
"""

import ctypes
import os
import threading

import psutil


class ThreadUtil:
    @staticmethod
    def terminate_thread(thread):
        """Terminates a python thread from another thread.

        :param thread: a threading.Thread instance
        """
        if not thread.is_alive():
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    @staticmethod
    def bg_run_task_on_thread(target: callable, args: iter):
        t = threading.Thread(target=target, args=args)
        t.daemon = True
        t.start()
        return t


class ProcessUtil:
    @staticmethod
    def cal_memory():
        """
        清除core日志文件，格式为core.xxx  https://github.com/microsoft/playwright/issues/9704
        Returns:
        """
        memory = "%0.1f MB" % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024)
        return memory
