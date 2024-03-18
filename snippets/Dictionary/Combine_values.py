#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：组合两个或多个字典，为每个键创建一个值列表。

解读：
创建一个新的collections.defaultdict，将list作为每个键的默认值，并循环遍历dict。
使用dict.append()将字典的值映射到键。
使用dict()将collections.defaultdict转换为普通字典。
"""
from collections import defaultdict


def combine_values(*dicts):
    res = defaultdict(list)
    for d in dicts:
        for key in d:
            res[key].append(d[key])
    return dict(res)


# Examples

d1 = {'a': 1, 'b': 'foo', 'c': 400}
d2 = {'a': 3, 'b': 200, 'd': 400}

print(combine_values(d1, d2))
# output:
# {'a': [1, 3], 'b': ['foo', 200], 'c': [400], 'd': [400]}
