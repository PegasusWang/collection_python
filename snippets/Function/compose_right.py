#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：执行从左到右的函数组合。

解读：
使用functools.reduce()执行从左到右的函数组合。
第一个(最左边)函数可以接受一个或多个参数;其余的函数必须是一元的。
"""
from functools import reduce


def compose_right(*fns):
    return reduce(lambda f, g: lambda *args: g(f(*args)), fns)


# Examples

add = lambda x, y: x + y
square = lambda x: x * x
add_and_square = compose_right(add, square)
print(add_and_square(1, 2))
# output:
# 9
