#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：生成一个等差数列的数字列表，该数列从给定的正整数开始，直到指定的极限。

解读：
使用range()和list()与适当的start、step和end值。
"""


def arithmetic_progression(n, lim):
    return list(range(n, lim + 1, n))


# Examples

print(arithmetic_progression(5, 25))
# output:
# [5, 10, 15, 20, 25]
