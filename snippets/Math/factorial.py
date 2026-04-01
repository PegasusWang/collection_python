#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：计算数字的阶乘。

解读：
使用递归。
如果num小于等于1，则返回1。
否则，返回num和num - 1的阶乘的乘积
如果num是负数或浮点数，则抛出异常。
"""


def factorial(num):
    if num < 0 or num % 1 != 0:
        raise Exception("Number can't be floating point or negative.")
    return 1 if num == 0 else num * factorial(num - 1)


# Examples

print(factorial(6))
# output:
# 720
