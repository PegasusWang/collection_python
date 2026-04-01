#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将字典转换为元组列表。

解读：
使用dict.items()和list()从给定的字典中获取一个元组列表。
"""


def dict_to_list(d):
    return list(d.items())


# Examples

d = {'one': 1, 'three': 3, 'five': 5, 'two': 2, 'four': 4}
print(dict_to_list(d))
# output:
# [('one', 1), ('three', 3), ('five', 5), ('two', 2), ('four', 4)]
