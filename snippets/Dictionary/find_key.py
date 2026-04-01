#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：在提供的字典中查找具有给定值的第一个键。

解读：
使用dictionary.items()和next()返回值为val的第一个键。
"""


def find_key(dict, val):
    return next(key for key, value in dict.items() if value == val)


# Examples

ages = {
    'Peter': 10,
    'Isabel': 11,
    'Anna': 9,
}
print(find_key(ages, 11))
# output:
# Isabel
