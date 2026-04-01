#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 类装饰器
import time


class deco_cls(object):
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        print("class decorator before function")
        f = self._func(*args, **kwargs)
        print("class decorator after function")
        return f


@deco_cls
def do_something(a, b, c):
    print(a)
    time.sleep(1)
    print(b)
    time.sleep(1)
    print(c)
    return a


if __name__ == '__main__':
    # 使用@
    f = do_something("1", "2", "3")
    print(f)
