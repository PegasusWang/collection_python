#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：反转具有非唯一的可哈希值的字典。

解读：
创建一个collections.defaultdict，其中list作为每个键的默认值。
使用dictionary.items()与循环结合使用dict.append()将字典的值映射到键。
使用dict()将collections.defaultdict转换为普通字典。
"""
from collections import defaultdict


def collect_dictionary(obj):
    inv_obj = defaultdict(list)
    for key, value in obj.items():
        inv_obj[value].append(key)
    return dict(inv_obj)


# Examples

ages = {
    'Peter': 10,
    'Isabel': 10,
    'Anna': 9,
}
print(collect_dictionary(ages))
# output:
# { 10: ['Peter', 'Isabel'], 9: ['Anna'] }
