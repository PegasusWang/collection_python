#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：使用提供的函数将每个元素映射到一个值后，计算列表的平均值。

解读：
使用map()将每个元素映射到fn返回的值。
使用sum()将所有映射值相加，除以len(lst)。
省略最后一个实参fn，使用默认的identity函数。
"""


def average_by(lst, fn=lambda x: x):
    return sum(map(fn, lst), 0.0) / len(lst)


# Examples

print(average_by([{'n': 4}, {'n': 2}, {'n': 8}, {'n': 6}], lambda x: x['n']))
# output:
# 5.0
