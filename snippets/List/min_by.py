#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：使用提供的函数将每个元素映射到一个值后，返回列表的最小值。

解读：
使用map()和fn，使用提供的函数将每个元素映射到一个值。
使用min()返回最小值。
"""


def min_by(lst, fn):
    return min(map(fn, lst))


# Examples

print(min_by([{'n': 4}, {'n': 2}, {'n': 8}, {'n': 6}], lambda v: v['n']))
# output:
# 2
