#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：使用提供的函数将每个元素映射到一个值后，返回列表的最大值。

解读：
使用map()和fn，使用提供的函数将每个元素映射到一个值。
使用max()返回最大值。
"""


def max_by(lst, fn):
    return max(map(fn, lst))


# Examples

print(max_by([{'n': 4}, {'n': 2}, {'n': 8}, {'n': 6}], lambda v: v['n']))
# output:
# 8
