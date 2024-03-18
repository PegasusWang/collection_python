#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：深层拼合列表

解读：
使用递归。
对collections.abc.Iterable使用isinstance()检查元素是否可迭代
如果是可迭代的，则递归应用deep_flatten()，否则返回[lst]。
"""
from collections.abc import Iterable


def deep_flatten(lst):
    return ([a for i in lst for a in deep_flatten(i)] if isinstance(lst, Iterable) else [lst])


# Examples

print(deep_flatten([1, [2], [[3], 4], 5]))
# output:
# [1, 2, 3, 4, 5]
