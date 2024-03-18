#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：针对测试函数测试一个值x，有条件地应用一个函数。

解读：
检查predicate(x)的值是否为True，如果为True则返回when_true(x)，否则返回x。
"""


def when(predicate, when_true):
    return lambda x: when_true(x) if predicate(x) else x


# Examples

double_even_numbers = when(lambda x: x % 2 == 0, lambda x: x * 2)
print(double_even_numbers(2))
print(double_even_numbers(1))
# output:
# 4
# 1
