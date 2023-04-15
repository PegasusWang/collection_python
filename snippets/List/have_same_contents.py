#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查两个列表是否包含相同的元素，而不考虑顺序。

解读：
对两个列表的组合使用set()来查找唯一的值。
使用for循环遍历它们，比较每个列表中每个唯一值的count()。
如果计数不匹配任何元素，则返回False，否则返回True。
"""


def have_same_contents(a, b):
    return all(a.count(v) == b.count(v) for v in set(a + b))


# Examples

print(have_same_contents([1, 2, 4], [2, 4, 1]))
# output:
# True
