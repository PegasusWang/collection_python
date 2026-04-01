#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将一个十六进制颜色码转换为一个与RGB分量对应的整数元组。

解读：
结合int()和列表切片表示法使用列表推导式从十六进制字符串中获取RGB分量。
使用tuple()将结果列表转换为元组。
"""


def hex_to_rgb(hex):
    return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))


# Examples

print(hex_to_rgb('FFA501'))
# output:
# (255, 165, 1)
