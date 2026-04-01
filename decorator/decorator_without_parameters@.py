#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 不带参数的装饰器
import time


def deco_test(func):
    def wrapper(*args, **kwargs):
        print("before function")
        f = func(*args, **kwargs)
        print("after function")
        return f
    return wrapper

@deco_test
def do_something(a,b,c):
    print(a)
    time.sleep(1)
    print(b)
    time.sleep(1)
    print(c)
    return a

if __name__ == '__main__':
    # 使用@
    f = do_something("1","2","3")
    print(f)