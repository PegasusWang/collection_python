#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：对二维列表进行转置。

解读：
使用*lst以元组的形式获取提供的列表。
结合使用zip()和list()来创建给定二维列表的转置。
"""


def transpose(lst):
    return list(zip(*lst))


# Examples

print(transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]))
# output:
# [(1, 4, 7, 10), (2, 5, 8, 11), (3, 6, 9, 12)]
