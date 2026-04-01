#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：合并两个或多个字典。

解读：
创建一个新的字典并循环遍历字典，使用dictionary.update()将每个字典的键值对添加到结果中。
"""


def merge_dictionaries(*dicts):
    res = {}
    for d in dicts:
        res |= d
    return res


# Examples

ages_one = {
    'Peter': 10,
    'Isabel': 11,
}
ages_two = {
    'Anna': 9
}
print(merge_dictionaries(ages_one, ages_two))
# output:
# { 'Peter': 10, 'Isabel': 11, 'Anna': 9 }
