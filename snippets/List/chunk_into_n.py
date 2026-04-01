#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将一个列表分成n个较小的列表。

解读：
使用math.ceil()和len()获取每个块的大小。
使用list()和range()创建一个大小为n的新列表。
使用map()将新列表的每个元素映射到一个大小为length的块
如果不能均匀地分割原始列表，则最后一个块将包含剩余的元素
"""
from math import ceil


def chunk_into_n(lst, n):
    size = ceil(len(lst) / n)
    return list(map(lambda x: lst[x * size:x * size + size], list(range(n))))


# Examples

print(chunk_into_n([1, 2, 3, 4, 5, 6, 7], 4))
# output:
# [[1, 2], [3, 4], [5, 6], [7]]
