#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回给定迭代器的幂集。

解读：
使用list()将给定值转换为list。
使用range()和itertools.combination()创建一个返回所有子集的生成器。
使用itertools.chain.from_iterable()和list()来使用生成器并返回一个列表。
"""
from itertools import chain, combinations


def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


# Examples

print(powerset([1, 2]))
# output:
# [(), (1,), (2,), (1, 2)]
