#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回列表中最常用的元素。

解读：
使用set()获取lst中唯一的值。
使用max()查找外观最多的元素。
"""


def most_frequent(lst):
    return max(set(lst), key=lst.count)


# Examples

print(most_frequent([1, 2, 1, 2, 3, 2, 1, 4, 2]))
# output：
# 2
