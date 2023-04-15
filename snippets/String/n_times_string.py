#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：生成一个字符串，该字符串重复n次给定的字符串值。

解读:
使用*操作符重复字符串n次。
"""


def n_times_string(s, n) -> str:
    return (s * n)


# Examples

print(n_times_string('py', 4))
# output:
# 'pypypypy'
