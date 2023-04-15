#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：创建平面字典中所有键的平面列表。

解读：
使用dict.keys()返回给定字典中的键值。
返回前一个结果的list()。
"""


def keys_only(flat_dict):
    return list(flat_dict.keys())


# Examples

ages = {
    'Peter': 10,
    'Isabel': 11,
    'Anna': 9,
}
print(keys_only(ages))
# output:
# ['Peter', 'Isabel', 'Anna']
