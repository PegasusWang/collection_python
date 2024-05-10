#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回字符串的长度（以字节为单位）。

解读:
使用str.encode('utf-8')对给定的字符串进行编码并返回其长度。
"""


def byte_size(s):
    return len(s.encode('utf-8'))


# Examples

print(byte_size('😀'))
print(byte_size('Hello World'))
# output:
# 4
# 11
