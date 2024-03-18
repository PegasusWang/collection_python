#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将指定数量的元素移动到列表的开头。

解读：
使用切片表示法获得列表的两个切片，并在返回之前组合它们。
"""


def roll(lst, offset):
    return lst[-offset:] + lst[:-offset]


# Examples

print(roll([1, 2, 3, 4, 5], 2))
print(roll([1, 2, 3, 4, 5], -2))
# output:
# [4, 5, 1, 2, 3]
# [3, 4, 5, 1, 2]
