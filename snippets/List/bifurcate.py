#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：根据给定筛选器列表的结果将值分成两组。

解读：
根据过滤器，使用列表推导和zip()将元素添加到组中。
如果filter对任何元素都有真值，则将其添加到第一个组，否则将其添加到第二个组。
"""


def bifurcate(lst, filter):
    return [
        [x for x, flag in zip(lst, filter) if flag],
        [x for x, flag in zip(lst, filter) if not flag]
    ]


# Examples

print(bifurcate(['beep', 'boop', 'foo', 'bar'], [True, True, False, True]))
# output:
# [ ['beep', 'boop', 'bar'], ['foo'] ]
