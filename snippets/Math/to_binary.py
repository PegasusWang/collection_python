#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回给定数字的二进制表示形式。

解读：
使用bin()将给定的十进制数转换为等效的二进制数。
"""


def to_binary(n):
    return bin(n)


# Examples

print(to_binary(100))
# output:
# 0b1100100
