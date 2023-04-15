#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：创建一个字典，其中列表的唯一值作为键，它们的频率作为值。

解读：
使用collections.defaultdict()来存储每个唯一元素的频率。
使用dict()返回一个字典，其中列表中唯一的元素作为键，它们的频率作为值。

该函数与collections.Counter功能一样
"""
from collections import defaultdict


def frequencies(lst):
    freq = defaultdict(int)
    for val in lst:
        freq[val] += 1
    return dict(freq)


# Examples

print(frequencies(['a', 'b', 'a', 'c', 'a', 'a', 'b']))
# output:
# { 'a': 4, 'b': 2, 'c': 1 }
