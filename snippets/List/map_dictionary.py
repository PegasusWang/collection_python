#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：使用函数将列表的值映射到字典，其中键-值对由原始值作为键，函数的结果作为值组成。

解读：
使用map()将fn应用到列表的每个值。
使用zip()将原始值与fn生成的值配对。
使用dict()返回一个合适的字典。
"""


def map_dictionary(itr, fn):
    return dict(zip(itr, map(fn, itr)))


# Examples

print(map_dictionary([1, 2, 3], lambda x: x * x))
# output:
# { 1: 1, 2: 4, 3: 9 }
