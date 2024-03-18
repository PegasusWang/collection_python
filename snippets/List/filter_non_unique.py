#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：创建一个包含过滤掉的非唯一值的列表

解读：
使用collections.Counter以获取列表中每个值的计数。
使用列表推导式创建只包含唯一值的列表。
"""
from collections import Counter


def filter_non_unique(lst):
    return [item for item, count in Counter(lst).items() if count == 1]


# Examples

print(filter_non_unique([1, 2, 2, 3, 4, 4, 5]))
# output:
# [1, 3, 5]
