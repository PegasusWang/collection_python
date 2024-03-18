#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回列表中某个元素出现的所有索引的列表。

解读：
使用enumerate()和一个列表推导式来检查每个元素是否与value相等，并在结果中添加i。
"""
def index_of_all(lst, value):
    return [i for i, x in enumerate(lst) if x == value]


# Examples

print(index_of_all([1, 2, 1, 4, 5, 1], 1))
print(index_of_all([1, 2, 3, 4], 6))
# output：
# [0, 2, 5]
# []
