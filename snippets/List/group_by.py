#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：根据给定的函数对列表中的元素进行分组。

解读：
使用collections.defaultdict初始化字典。
结合使用fn与for循环和dict.append()来填充字典。
使用dict()将其转换为普通字典。
"""
from collections import defaultdict
from math import floor


def group_by(lst, fn):
    d = defaultdict(list)
    for el in lst:
        d[fn(el)].append(el)
    return dict(d)


# Examples

print(group_by([6.1, 4.2, 6.3], floor))
print(group_by(['one', 'two', 'three'], len))
# output:
# {4: [4.2], 6: [6.1, 6.3]}
# {3: ['one', 'two'], 5: ['three']}
