#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回列表中除最后一个元素外的所有元素。

解读：
使用lst[:-1]返回列表中除最后一个元素外的所有元素。
"""


def initial(lst):
    return lst[:-1]


# Examples

print(initial([1, 2, 3]))
# output：
# [1, 2]
