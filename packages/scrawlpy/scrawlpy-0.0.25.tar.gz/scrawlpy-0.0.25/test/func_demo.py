# -*- coding: utf-8 -*-
# @Time   : 2024/4/30 18:44
import time

import func_timeout
from func_timeout import func_set_timeout

timeout = 3


@func_set_timeout(timeout)  # 设定函数执行时间
def task():
    print('开始运行！')
    time.sleep(5)
    return '执行成功，未超时'


try:
    result = task()
    print(result)
except (Exception, func_timeout.exceptions.FunctionTimedOut) as e:
    print(e)
