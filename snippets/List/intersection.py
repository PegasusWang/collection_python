#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回两个列表中都存在的元素列表。

解读：
从a和b创建一个集合
使用内置的集合运算符＆仅保留两个集合中包含的值，然后将集合转换回列表。
"""


def intersection(a, b):
    _a, _b = set(a), set(b)
    return list(_a & _b)


# Examples

print(intersection([1, 2, 3], [4, 3, 2]))
# output:
# [2, 3]
