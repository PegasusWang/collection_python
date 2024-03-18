#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：根据给定的过滤函数的结果将值分成两组。

解读：
根据fn为每个元素返回的值，使用列表推导式将元素添加到组中。
如果fn为任何元素返回真值，则将其添加到第一组，否则将其添加到第二组。
"""


def bifurcate_by(lst, fn):
    return [
        [x for x in lst if fn(x)],
        [x for x in lst if not fn(x)]
    ]


# Examples

print(bifurcate_by(['beep', 'boop', 'foo', 'bar'], lambda x: x[0] == 'b'))
# output:
# [ ['beep', 'boop', 'bar'], ['foo'] ]
