#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将字典列表转换为与指定键对应的值列表。

解读：
使用列表推导式和dict.get()来获取lst中每个字典的key值。
"""


def pluck(lst, key):
    return [x.get(key) for x in lst]


# Examples

simpsons = [
    {'name': 'lisa', 'age': 8},
    {'name': 'homer', 'age': 36},
    {'name': 'marge', 'age': 34},
    {'name': 'bart', 'age': 10}
]
print(pluck(simpsons, 'age'))
# output:
# [8, 36, 34, 10]
