#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：创建具有与提供的字典相同的键的字典，并为每个值运行通过提供的函数生成的值。

解读：
使用dict.items()遍历字典，将fn生成的值赋给新字典的每个键。
"""


def map_values(obj, fn):
    return {k: fn(v) for k, v in obj.items()}


# Examples

users = {
    'fred': {'user': 'fred', 'age': 40},
    'pebbles': {'user': 'pebbles', 'age': 1}
}
print(map_values(users, lambda u: u['age']))
# output:
# {'fred': 40, 'pebbles': 1}
