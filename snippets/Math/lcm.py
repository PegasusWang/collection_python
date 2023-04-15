#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回数字列表的最小公倍数。

解读：
在给定的列表上使用functools.reduce()， math.gcd()和lcm(x,y) = x * y / gcd(x,y)。
"""
from functools import reduce
from math import gcd


def lcm(numbers):
    return reduce((lambda x, y: int(x * y / gcd(x, y))), numbers)


# Examples

print(lcm([12, 7]))
print(lcm([1, 3, 4, 5]))
# output:
# 84
# 60
