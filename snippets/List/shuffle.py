#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：随机化列表中值的顺序，返回一个新的列表。

解读：
使用Fisher-Yates算法对列表中的元素重新排序。
random.shuffle提供了与此代码片段类似的功能。
"""
from copy import deepcopy
from random import randint


def shuffle(lst):
    temp_lst = deepcopy(lst)
    m = len(temp_lst)
    while (m):
        m -= 1
        i = randint(0, m)
        temp_lst[m], temp_lst[i] = temp_lst[i], temp_lst[m]
    return temp_lst


# Examples

foo = [1, 2, 3]
print(shuffle(foo), f', foo = {foo}')
# output:
# [2, 3, 1], foo = [1, 2, 3]
