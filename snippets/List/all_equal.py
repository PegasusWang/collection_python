#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查列表中的所有元素是否相等。

解读：
使用set()消除重复的元素，然后使用len()检查length是否为1。
"""


def all_equal(lst):
    return len(set(lst)) == 1


# Examples

print(all_equal([1, 2, 3, 4, 5, 6]))
print(all_equal([1, 1, 1, 1]))
# output:
# False
# True
