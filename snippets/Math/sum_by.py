#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：使用提供的函数将每个元素映射到一个值之后，计算列表的总和。

解读：
使用map()和fn，使用提供的函数将每个元素映射到一个值。
使用sum()返回值的和。
"""


def sum_by(lst, fn):
    return sum(map(fn, lst))


# Examples

print(sum_by([{'n': 4}, {'n': 2}, {'n': 8}, {'n': 6}], lambda v: v['n']))
# output:
# 20
