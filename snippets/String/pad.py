#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：如果指定的字符比指定的长度短，则在字符串的两边填充指定的字符。

解读:
使用str.ljust()和str.rjust()来填充给定字符串的两边。
省略第三个参数char，以使用空白字符作为默认填充字符。
"""
from math import floor


def pad(s, length, char=' ')->str:
    return s.rjust(floor((len(s) + length) / 2), char).ljust(length, char)


# Examples

print(repr(pad('cat', 8)))
print(repr(pad('42', 6, '0')))
print(repr(pad('foobar', 3)))
# output:
# '  cat   '
# '004200'
# 'foobar'
