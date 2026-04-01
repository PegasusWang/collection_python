#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：初始化一个列表，该列表包含指定范围内的数字，其中start和end包含它们的共同差值步骤。

解读：
使用list()和range()生成一个适当长度的列表，在给定的范围内填充所需的值。
省略start以使用默认值0
省略步长，使用默认值1
"""


def initialize_list_with_range(end, start=0, step=1):
    return list(range(start, end + 1, step))


# Examples

print(initialize_list_with_range(5))
print(initialize_list_with_range(7, 3))
print(initialize_list_with_range(9, 0, 2))
# output:
# [0, 1, 2, 3, 4, 5]
# [3, 4, 5, 6, 7]
# [0, 2, 4, 6, 8]
