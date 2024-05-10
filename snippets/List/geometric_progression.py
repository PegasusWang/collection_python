#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：初始化一个列表，该列表包含指定范围内的数字，其中包括起始和结束，两个术语之间的比率为step。如果step = 1，则返回错误。

解读：
使用range()、math.log()和math.floor()以及一个列表推导式来创建一个适当长度的列表，并为每个元素应用step。
忽略第二个参数start，使用默认值1。
忽略第三个参数step，使用默认值2。
"""
from math import floor, log


def geometric_progression(end, start=1, step=2):
    return [start * step**i for i in range(floor(log(end / start) / log(step)) + 1)]


# Examples

print(geometric_progression(256))
print(geometric_progression(256, 3))
print(geometric_progression(256, 1, 4))
# output:
# [1, 2, 4, 8, 16, 32, 64, 128, 256]
# [3, 6, 12, 24, 48, 96, 192]
# [1, 4, 16, 64, 256]
