#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：查找给定列表中满足所提供的测试函数的所有元素的索引。

解读：
使用enumerate()和一个列表推导式来返回fn返回True的lst中所有元素的索引。
"""


def find_index_of_all(lst, fn):
    return [i for i, x in enumerate(lst) if fn(x)]


# Examples

print(find_index_of_all([1, 2, 3, 4], lambda n: n % 2 == 1))
# output:
# [0, 2]
