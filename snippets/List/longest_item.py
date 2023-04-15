#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：接受任意数量的可迭代对象或带有length属性的对象，并返回最长的那个。

解读：
使用max()和len()作为键来返回最大长度的项。
如果多个对象具有相同的长度，则返回第一个对象。
"""


def longest_item(*args):
    return max(args, key=len)


# Examples

print(longest_item('this', 'is', 'a', 'testcase'))
print(longest_item([1, 2, 3], [1, 2], [1, 2, 3, 4, 5]))
print(longest_item([1, 2, 3], 'foobar'))
# output:
# testcase
# [1, 2, 3, 4, 5]
# foobar
