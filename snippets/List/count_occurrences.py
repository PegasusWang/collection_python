#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：计算列表中出现的值。

解读：
使用list.count()来计算val在lst中出现的次数。
"""


def count_occurrences(lst, val):
    return lst.count(val)


# Examples

print(count_occurrences([1, 1, 2, 1, 2, 3], 1))
# output:
# 3
