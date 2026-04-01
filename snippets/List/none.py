#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查所提供的函数是否对列表中至少一个元素返回True。

解读：
使用all()和fn检查fn是否为列表中的所有元素返回False。
"""


def none(lst, fn=lambda x: x):
    return all(not fn(x) for x in lst)


# Examples

print(none([0, 1, 2, 0], lambda x: x >= 2))
print(none([0, 0, 0]))
# output:
# False
# True
