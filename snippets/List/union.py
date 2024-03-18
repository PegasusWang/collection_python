#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回两个列表中存在的每个元素一次

解读：
创建一个包含a和b的所有值的集合，并将其转换为一个列表。
"""


def union(a, b):
    return list(set(a + b))


# Examples

print(union([1, 2, 3], [4, 3, 2]))
# output:
# [1, 2, 3, 4]
