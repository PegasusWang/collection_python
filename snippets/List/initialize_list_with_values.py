#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：初始化并使用指定的值填充列表。

解读：
使用列表推导式和range()生成一个长度等于n的列表，并填充所需的值。
省略val，使用默认值0。
"""


def initialize_list_with_values(n, val=0):
    return [val for _ in range(n)]


# Examples

print(initialize_list_with_values(5, 2))
# output:
# [2, 2, 2, 2, 2]
