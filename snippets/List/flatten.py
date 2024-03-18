#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：把列表的列表变平一次。

解读：
使用列表推导式按顺序从子列表中提取每个值。
"""


def flatten(lst):
    return [x for y in lst for x in y]


# Examples

print(flatten([[1, 2, 3, 4], [5, 6, 7, 8]]))
# output:
# [1, 2, 3, 4, 5, 6, 7, 8]
