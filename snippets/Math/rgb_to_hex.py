#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将RGB分量的值转换为十六进制颜色码。

解读：
使用'{:02X}'为零填充的十六进制值创建一个占位符，并将其复制三次。
对结果字符串使用str.format()将占位符替换为给定的值。
"""


def rgb_to_hex(r, g, b):
    return ('{:02X}' * 3).format(r, g, b)


# Examples

print(rgb_to_hex(255, 165, 1))
# output:
# FFA501
