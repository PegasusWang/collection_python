#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回列表中具有最大值的元素的索引。

解读：
使用max()和list.index()获取列表中的最大值并返回其索引。
"""


def max_element_index(arr):
    return arr.index(max(arr))


# Examples

print(max_element_index([5, 8, 9, 7, 10, 3, 0]))
# output:
# 4
