#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回一个从开头移除n个元素的列表

解读：
使用切片表示法创建一个包含n个从开始取的元素的列表切片。
"""


def take(itr, n=1):
    return itr[:n]


# Examples

print(take([1, 2, 3], 5))
print(take([1, 2, 3], 0))
# output:
# [1, 2, 3]
# []
