#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回给定数字的十六进制表示形式

解读：
使用hex()将给定的十进制数转换为其等效的十六进制数
"""


def to_hex(dec):
    return hex(dec)


# Examples

print(to_hex(41))
print(to_hex(332))
# output:
# 0x29
# 0x14c
