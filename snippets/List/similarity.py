#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回两个列表中都存在的元素列表。

解读：
对a使用列表推导式，只保留包含在两个列表中的值
"""


def similarity(a, b):
    return [item for item in a if item in b]


# Examples

print(similarity([1, 2, 3], [1, 2, 4]))
# output:
# [1, 2]
