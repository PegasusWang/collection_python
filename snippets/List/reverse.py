#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：反转列表或字符串。

解读:
使用切片表示法反转列表或字符串。
"""


def reverse(itr):
    return itr[::-1]


# Examples

print(reverse([1, 2, 3]))
print(reverse('snippet'))
# output:
# [3, 2, 1]
# teppins
