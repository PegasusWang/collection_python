#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：初始化给定宽度、高度和值的2D列表。

解读：
使用列表推导式和range()生成h行，其中每一行都是长度为h的列表，用val初始化。
忽略最后一个参数val，将默认值设置为None。
"""


def initialize_2d_list(w, h, val=None):
    return [[val for _ in range(w)] for _ in range(h)]


# Examples

print(initialize_2d_list(2, 2, 0))
# output:
# [[0, 0], [0, 0]]
