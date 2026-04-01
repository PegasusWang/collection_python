#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回给定列表中的唯一元素

解读：
从列表中创建一个集合来丢弃重复的值，然后从中返回一个列表。
"""


def unique_elements(li):
    return list(set(li))


# Examples

print(unique_elements([1, 2, 2, 3, 4, 3]))
# output:
# [1, 2, 3, 4]
