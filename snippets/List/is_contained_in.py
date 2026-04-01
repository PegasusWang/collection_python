#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查第一个列表的元素是否包含在第二个列表中，而不考虑顺序。

解读：
使用count()检查某个值在a中的出现次数是否多于在b中的出现次数。
如果找到任何这样的值则返回False，否则返回True。
"""


def is_contained_in(a, b):
    return all(a.count(v) <= b.count(v) for v in set(a))


# Examples

print(is_contained_in([1, 4], [2, 4, 1]))
# output:
# True
