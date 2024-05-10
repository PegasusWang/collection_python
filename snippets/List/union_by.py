#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将提供的函数应用到两个列表中的每个元素之后，一次返回两个列表中任何一个列表中存在的每个元素。

解读：
通过对a中的每个元素应用fn创建一个集合。
在b上结合使用一个列表推导式和fn来只保留先前创建的集合_a中不包含的值。
最后，从前面的结果和a创建一个集合，并将其转换为一个列表
"""
from math import floor


def union_by(a, b, fn):
    _a = set(map(fn, a))
    return list(set(a + [item for item in b if fn(item) not in _a]))


# Examples

print(union_by([2.1], [1.2, 2.3], floor))
# output:
# [2.1, 1.2]
