#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将提供的函数应用于两个列表的每个列表元素后，返回两个列表中存在的元素列表。

解读：
创建一个集合，使用map()将fn应用到b中的每个元素。
在a上结合使用一个列表推导式和fn来只保留包含在两个列表中的值。
"""
from math import floor


def intersection_by(a, b, fn):
    _b = set(map(fn, b))
    return [item for item in a if fn(item) in _b]


# Examples

print(intersection_by([2.1, 1.2], [2.3, 3.4], floor))
# output:
# [2.1]
