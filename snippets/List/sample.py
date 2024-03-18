#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：从列表中返回一个随机元素。

解读：
使用random.choice()从lst中获取一个随机元素
"""
from random import choice


def sample(lst):
    return choice(lst)


# Examples

print(sample([3, 7, 9, 11]))
# output:
# 9
