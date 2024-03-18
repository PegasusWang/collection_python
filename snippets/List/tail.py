#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回列表中除第一个元素外的所有元素。

解读：
如果列表的长度大于1，则使用切片表示法返回最后一个元素。
否则，返回整个列表。
"""


def tail(lst):
    return lst[1:] if len(lst) > 1 else lst


# Examples

print(tail([1, 2, 3]))
print(tail([1]))
# output:
# [2, 3]
# [1]
