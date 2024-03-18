#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：在字典中查找最小值的键。

解读：
使用min()并将key参数设置为dict.get()来查找并返回给定字典中最小值的键。
"""


def key_of_min(d):
    return min(d, key=d.get)


# Examples

print(key_of_min({'a': 4, 'b': 0, 'c': 13}))
# output:
# b
