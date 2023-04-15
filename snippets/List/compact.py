#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：从列表中删除假值。

解读：
使用filter()过滤掉假值(False、None、0和"")。
"""


def compact(lst):
    return list(filter(None, lst))


# Examples

print(compact([0, 1, False, 2, '', 3, 'a', 's', 34]))
# output:
# [ 1, 2, 3, 'a', 's', 34 ]
