#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回平面字典中所有值的平面列表。

解读：
使用dict.values()返回给定字典中的值。
返回前一个结果的list()。
"""


def values_only(flat_dict):
    return list(flat_dict.values())


# Examples

ages = {
    'Peter': 10,
    'Isabel': 11,
    'Anna': 9,
}
print(values_only(ages))
# output:
# [10, 11, 9]
