#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查平面列表中是否有重复的值。

解读：
在给定的列表中使用set()删除重复项，并将其长度与列表长度进行比较。
"""


def has_duplicates(lst):
    return len(lst) != len(set(lst))


# Examples

x = [1, 2, 3, 4, 5, 5]
y = [1, 2, 3, 4, 5]
print(has_duplicates(x))
print(has_duplicates(y))
# output:
# True
# False
