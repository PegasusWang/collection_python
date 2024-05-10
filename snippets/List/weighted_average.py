#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回两个或多个数字的加权平均值。

解读：
使用sum()可以按权重对数字乘积求和，然后对权重求和。
使用zip()和列表推导式来迭代值和权重对
"""


def weighted_average(nums, weights):
    return sum(x * y for x, y in zip(nums, weights)) / sum(weights)


# Examples

print(weighted_average([1, 2, 3], [0.6, 0.2, 0.3]))
# output:
# 1.727272727272727
