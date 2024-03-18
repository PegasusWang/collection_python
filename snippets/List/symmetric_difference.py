#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回两个可迭代对象之间的对称差，而不会过滤出重复的值。

解读：
从每个列表创建一个集合。
对它们中的每一个都使用列表推导式，以只保留先前创建的另一个集合中不包含的值。
"""


def symmetric_difference(a, b):
    (_a, _b) = (set(a), set(b))
    return [item for item in a if item not in _b] + [item for item in b if item not in _a]


# Examples

print(symmetric_difference([1, 2, 3], [1, 2, 4]))
# output:
# [3, 4]
