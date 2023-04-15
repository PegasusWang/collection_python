#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将数字转换为数字列表。

解读：
对n的字符串表示形式使用map()和int组合，并从结果返回一个列表。
"""


def digitize(n):
    return list(map(int, str(n)))


# Examples

print(digitize(123))
# output:
# [1, 2, 3]
