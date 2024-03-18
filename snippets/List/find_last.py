#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：查找给定列表中满足所提供的测试函数的最后一个元素的值。

解读：
使用列表推导式和next()返回lst中fn返回True的最后一个元素。
"""


def find_last(lst, fn):
    return next(x for x in lst[::-1] if fn(x))


# Examples

print(find_last([1, 2, 3, 4], lambda n: n % 2 == 1))
# output:
# 3
