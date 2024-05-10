#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：查找给定列表中满足所提供的测试函数的最后一个元素的索引。

解读：
使用列表推导式、enumerate()和next()返回lst中fn返回True的最后一个元素的索引。
"""


def find_last_index(lst, fn):
    return len(lst) - 1 - next(i for i, x in enumerate(lst[::-1]) if fn(x))


# Examples

print(find_last_index([1, 2, 3, 4], lambda n: n % 2 == 1))
# output:
# 2
