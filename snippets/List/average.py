#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：计算两个或多个数字的平均值。

解读：
使用sum()将提供的所有参数相加，除以len()。
"""


def average(*args):
    return sum(args, 0.0) / len(args)


# Examples

print(average(*[1, 2, 3]))
print(average(1, 2, 3))
# output:
# 2.0
# 2.0
