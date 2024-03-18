#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将给定数字填充到指定长度。

解读:
在将数字转换为字符串之后，使用str.zfill()将数字填充为指定的长度。
"""


def pad_number(n, l) -> str:
    return str(n).zfill(l)


# Examples

print(pad_number(1234, 6))
# output:
# 001234
