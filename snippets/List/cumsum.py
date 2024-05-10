#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：创建部分和的列表。

解读：
使用itertools.accumulate()创建每个元素的累积和。
使用list()将结果转换为列表。
"""
from itertools import accumulate


def cumsum(lst):
    return list(accumulate(lst))


# Examples

print(cumsum(range(0, 15, 3)))
# output:
# [0, 3, 9, 18, 30]
