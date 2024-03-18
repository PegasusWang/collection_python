#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将提供的函数应用于两个列表的每个元素后，返回两个列表之间的差异。

解读：
创建一个集合，使用map()将fn应用到b中的每个元素。
在a上与fn结合使用一个列表推导式，只保留前面创建的集合_b中不包含的值。
"""
from math import floor


def difference_by(a, b, fn):
    _b = set(map(fn, b))
    return [item for item in a if fn(item) not in _b]


# Examples

print(difference_by([2.1, 1.2], [2.3, 3.4], floor))
print(difference_by([{'x': 2}, {'x': 1}], [{'x': 1}], lambda v: v['x']))
# output:
# [1.2]
# [{'x': 2}]
