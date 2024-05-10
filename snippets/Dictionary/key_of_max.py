#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：查找字典中最大值的键。

解读:
使用max()并将key参数设置为dict.get()来查找并返回给定字典中最大值的键。
"""


def key_of_max(d):
    return max(d, key=d.get)


# Examples

print(key_of_max({'a': 4, 'b': 0, 'c': 13}))
# output:
# c
