#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：创建一个包含过滤掉的唯一值的列表。

解读：
使用collections.Counter获取列表中每个值的计数。
使用列表推导式来创建仅包含非唯一值的列表。
"""
from collections import Counter


def filter_unique(lst):
    return [item for item, count in Counter(lst).items() if count > 1]


# Examples

print(filter_unique([1, 2, 2, 3, 4, 4, 5]))
# output:
# [2, 4]
