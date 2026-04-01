#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：对每个列表元素执行一次提供的函数

解读：
使用for循环对itr中的每个元素执行fn。
"""


def for_each(itr, fn):
    for el in itr:
        fn(el)


# Examples

for_each([1, 2, 3], print)
# output:
# 1 2 3
