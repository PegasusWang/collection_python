#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：计算两个可迭代对象之间的差值，不过滤重复值。

解读：
从b创建一个集合。
对a使用列表推导式，只保留前面创建的集合_b中不包含的值。
"""


def difference(a, b):
    _b = set(b)
    return [item for item in a if item not in _b]


# Examples

print(difference([1, 2, 3], [1, 2, 4]))
# output:
# [3]
