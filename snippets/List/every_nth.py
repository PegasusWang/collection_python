#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回列表中的每个第n个元素

解读：
使用切片表示法创建一个新列表，该列表包含给定列表的第n个元素。
"""


def every_nth(lst, nth):
    return lst[nth - 1::nth]


# Examples

print(every_nth([1, 2, 3, 4, 5, 6], 2))
# output:
# [ 2, 4, 6 ]
