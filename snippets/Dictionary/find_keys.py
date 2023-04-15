#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：在提供的字典中查找具有给定值的所有键。

解读：
使用dictionary.items()，生成器和list()返回所有值等于val的键。
"""


def find_keys(dict, val):
    return [key for key, value in dict.items() if value == val]


# Examples

ages = {
    'Peter': 10,
    'Isabel': 11,
    'Anna': 10,
}
print(find_keys(ages, 10))
# output:
# [ 'Peter', 'Anna' ]
