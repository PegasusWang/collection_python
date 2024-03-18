#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将提供的函数应用于两个列表的每个列表元素后，返回两个列表之间的对称差异。

解读：
通过对每个列表中的每个元素应用fn来创建一个集合。
将列表推导与fn一起使用时，仅保留先前创建的另一个列表中未包含的值。
"""
from math import floor


def symmetric_difference_by(a, b, fn):
    (_a, _b) = (set(map(fn, a)), set(map(fn, b)))
    return [item for item in a if fn(item) not in _b] + [item for item in b if fn(item) not in _a]


# Examples

print(symmetric_difference_by([2.1, 1.2], [2.3, 3.4], floor))
# output:
# [1.2, 3.4]
