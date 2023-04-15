#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：根据给定的函数对列表中的元素进行分组，并返回每个组中的元素计数。

解读：
使用collections.defaultdict初始化字典。
使用map()去给定函数映射给定列表的值。

"""
from collections import defaultdict
from math import floor


def count_by(lst, fn=lambda x: x):
    count = defaultdict(int)
    for val in map(fn, lst):
        count[val] += 1
    return dict(count)


# Examples

print(count_by([6.1, 4.2, 6.3], floor))
print(count_by(['one', 'two', 'three'], len))
# output:
# {6: 2, 4: 1}
# {3: 2, 5: 1}
