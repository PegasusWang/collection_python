#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：如果提供的值不是列表，则将其转换为列表。

解读：
使用isinstance()检查给定的值是否为可枚举的。
使用list()返回或相应地封装在一个列表中。
"""


def cast_list(val):
    return list(val) if isinstance(val, (tuple, list, set, dict)) else [val]


# Examples

print(cast_list('foo'))
print(cast_list([1]))
print(cast_list(('foo', 'bar')))
# output:
# ['foo']
# [1]
# ['foo', 'bar']
