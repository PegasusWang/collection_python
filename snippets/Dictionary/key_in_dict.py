#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查给定的键是否存在于字典中。

解读：
使用in操作符检查d是否包含key。
"""


def key_in_dict(d, key):
    return (key in d)

#
# Examples

d = {'one': 1, 'three': 3, 'five': 5, 'two': 2, 'four': 4}
print(key_in_dict(d, 'three'))
# output:
# True
