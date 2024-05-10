#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回一个从末尾移除n个元素的列表。

解读：
使用切片表示法创建一个包含从末尾取的n个元素的列表切片。
"""


def take_right(itr, n=1):
    return itr[-n:]


# Examples

print(take_right([1, 2, 3], 2))
print(take_right([1, 2, 3]))
# output:
# [2, 3]
# [3]
