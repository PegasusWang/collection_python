#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：计算两个值之间的汉明距离。

解读：
使用异或运算符(^)找出两个数之间的位差。
使用bin()将结果转换为二进制字符串。
将字符串转换为列表，并使用str类的count()计数并返回其中的1的数量。
"""


def hamming_distance(a, b):
    return bin(a ^ b).count('1')


# Examples

print(hamming_distance(2, 3))
# output:
# 1
