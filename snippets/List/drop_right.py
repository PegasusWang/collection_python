#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回一个从右侧删除n个元素的列表

解读：
使用切片表示法从右侧删除指定数量的元素。
忽略最后一个参数n，使用默认值1。
"""


def drop_right(a, n=1):
    return a[:-n]


# Examples

print(drop_right([1, 2, 3]))
print(drop_right([1, 2, 3], 2))
print(drop_right([1, 2, 3], 42))
# output:
# [1, 2]
# [1]
# []
