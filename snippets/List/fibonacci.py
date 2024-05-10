#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：生成一个列表，包含斐波那契序列，直到第n项。

解读：
从0和1开始，使用list.append()将列表最后两个数字的总和加到列表的末尾，直到列表的长度达到n。
如果n小于或等于0，返回一个包含0的列表。
"""


def fibonacci(n):
    if n <= 0:
        return [0]
    sequence = [0, 1]
    while len(sequence) <= n:
        next_value = sequence[-1] + sequence[len(sequence) - 2]
        sequence.append(next_value)
    return sequence


# Examples

print(fibonacci(7))
# output:
# [0, 1, 1, 2, 3, 5, 8, 13]
