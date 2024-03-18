#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回不重复且无顺序地从 n 项中选择 k 项的方式总数

解读：
使用math.comb()计算二项式系数
注意：
comb是python3.8新版功能.
"""
from math import comb


def binomial_coefficient(n, k):
    return comb(n, k)


# Examples

print(binomial_coefficient(8, 2))
# output:
# 28
