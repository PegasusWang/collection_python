#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查提供的整数是否为质数。

解读：
如果数字是0、1、负数或2的倍数则返回False。
使用all()和range()检查从3到给定数字的平方根的数字。
如果没有除数则返回True，否则返回False。
"""
from math import sqrt


def is_prime(n):
    if n <= 1 or (n % 2 == 0 and n > 2):
        return False
    return all(n % i for i in range(3, int(sqrt(n)) + 1, 2))


# Examples

print(is_prime(11))
# output:
# True
