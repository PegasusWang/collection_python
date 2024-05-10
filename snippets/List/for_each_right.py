#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：对每个列表元素执行一次提供的函数，从列表的最后一个元素开始。

解读：
结合使用for循环和slice符号对itr中的每个元素执行fn，从最后一个元素开始。
"""


def for_each_right(itr, fn):
    for el in itr[::-1]:
        fn(el)


# Examples

for_each_right([1, 2, 3], print)
# output:
# 3 2 1
