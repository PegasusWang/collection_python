#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回提供的列表中的n个最大元素。

解读：
使用sorted()对列表进行排序。
使用切片表示法获得指定数量的元素
省略第二个参数n，得到一个只有一个元素的列表。
如果n大于或等于提供的列表的长度，则返回原始列表(按降序排序)。
"""


def max_n(lst, n=1):
    return sorted(lst, reverse=True)[:n]


# Examples

print(max_n([1, 2, 3]))
print(max_n([1, 2, 3], 2))
# output:
# [3]
# [3, 2]
