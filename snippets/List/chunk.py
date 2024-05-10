#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将列表分割成指定大小的较小列表。

解读：
使用list()和range()创建所需大小的列表。
在列表上使用map()，并使用给定列表的拼接来填充它。
最后，返回创建的列表。
"""
from math import ceil


def chunk(lst, size):
    return list(map(lambda x: lst[x * size:x * size + size], list(range(ceil(len(lst) / size)))))


# Examples

print(chunk([1, 2, 3, 4, 5], 2))
# output:
# [[1, 2], [3, 4], [5]]
