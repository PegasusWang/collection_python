#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查列表中的所有值是否都是唯一的。

解读：
在给定的列表中使用set()来保持唯一的出现。
使用len()将唯一值的长度与原始列表进行比较。
"""


def all_unique(lst):
    return len(lst) == len(set(lst))


# Examples

x = [1, 2, 3, 4, 5, 6]
y = [1, 2, 2, 3, 4, 5]
print(all_unique(x))
print(all_unique(y))
# output:
# True
# False
