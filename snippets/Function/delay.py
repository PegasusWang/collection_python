#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：以毫秒为单位调用所提供的函数。

解读：
使用time.sleep()将fn的执行延迟ms / 1000秒。
"""
from time import sleep


def delay(fn, ms, *args):
    sleep(ms / 1000)
    return fn(*args)


# Examples

delay(lambda x: print(x), 1000, 'later')
# output:
# prints 'later' after one second
