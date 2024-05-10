#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回列表中具有最小值的元素的索引。

解读：
使用min()和list.index()获取列表中的最小值，然后返回其索引。
"""


def min_element_index(arr):
    return arr.index(min(arr))


# Examples

print(min_element_index([3, 5, 2, 6, 10, 7, 9]))
# output:
# 2
