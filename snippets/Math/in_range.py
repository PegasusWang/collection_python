#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查给定数字是否在给定范围内。

解读：
使用算术比较检查给定的数字是否在指定的范围内。
如果没有指定第二个参数end，则该范围被认为是从0到start。
"""


def in_range(n, start, end=0):
    return start <= n <= end if end >= start else end <= n <= start


# Examples

print(in_range(3, 2, 5))
print(in_range(3, 4))
print(in_range(2, 3, 5))
print(in_range(3, 2))
# output:
# True
# True
# False
# False
