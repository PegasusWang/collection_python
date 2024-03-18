#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：咖喱一个函数。

解读：
使用functools.partial()返回一个新的partial对象，它的行为与fn类似，只是部分应用了给定的参数args。
"""
from functools import partial


def curry(fn, *args):
    return partial(fn, *args)


# Examples

add = lambda x, y: x + y
add10 = curry(add, 10)
print(add10(20))
# output:
# 30
