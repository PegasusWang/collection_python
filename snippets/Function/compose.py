#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：执行从右到左的函数组合。

解读：
使用functools.reduce()执行从右到左的函数组合。
最后一个(最右边的)函数可以接受一个或多个参数;其余的函数必须是一元的。
"""
from functools import reduce


def compose(*fns):
    return reduce(lambda f, g: lambda *args: f(g(*args)), fns)


# Examples

add5 = lambda x: x + 5
multiply = lambda x, y: x * y
multiply_and_add_5 = compose(add5, multiply)
print(multiply_and_add_5(5, 2))
# output:
# 15
