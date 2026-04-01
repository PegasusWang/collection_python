#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查所提供的函数是否对列表中至少一个元素返回True。

解读：
结合使用any()和map()检查fn是否为列表中的任何元素返回True
"""


def some(lst, fn=lambda x: x):
    return any(map(fn, lst))


# Examples

print(some([0, 1, 2, 0], lambda x: x >= 2))
print(some([0, 0, 1, 0]))
# output:
# True
# True
