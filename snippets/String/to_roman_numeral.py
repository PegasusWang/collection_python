#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将一个整数转换为它的罗马数字表示形式。接受1到3999之间的值(包括两个值)。

解读：
创建一个以(罗马值，整数)的形式包含元组的查找列表。
使用for循环在查找时遍历值。
使用divmod()用余数更新num，将罗马数字表示形式添加到结果中。
"""


def to_roman_numeral(num):
    lookup = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I'),
    ]
    res = ''
    for (n, roman) in lookup:
        (d, num) = divmod(num, n)
        res += roman * d
    return res


# Examples

print(to_roman_numeral(3))
print(to_roman_numeral(11))
print(to_roman_numeral(1998))
# output:
# III
# XI
# MCMXCVIII
