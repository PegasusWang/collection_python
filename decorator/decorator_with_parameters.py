#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 带参数的装饰器
import time


def logging(level):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            print("[{level}]: enter function {func}()".format(level=level, func=func.__name__))
            f = func(*args, **kwargs)
            print("after function: [{level}]: enter function {func}()".format(level=level, func=func.__name__))
            return f

        return inner_wrapper

    return wrapper


@logging(level="debug")
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
