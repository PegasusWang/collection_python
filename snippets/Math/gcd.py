#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：计算数字列表的最大公约数。

解读：
在给定列表上使用functools.reduce()和math.gcd()。
"""
from functools import reduce
from math import gcd as _gcd


def gcd(numbers):
    return reduce(_gcd, numbers)


# Examples

print(gcd([8, 36, 28]))
# output:
# 4
