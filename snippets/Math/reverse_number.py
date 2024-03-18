#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：反转数字。

解读：
使用str()将数字转换为字符串，使用slice表示法将其颠倒，使用str.replace()删除符号。
使用float()将结果转换为浮点数字，使用math.copysign()复制原始符号。
"""
from math import copysign


def reverse_number(n) -> float:
    return copysign(float(str(n)[::-1].replace('-', '')), n)


# Examples

print(reverse_number(981))
print(reverse_number(-500))
print(reverse_number(73.6))
print(reverse_number(-5.23))
# output:
# 189.0
# -5.0
# 6.37
# -32.5
