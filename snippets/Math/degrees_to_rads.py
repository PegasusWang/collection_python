#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将角度从角度转换为弧度。

解读：
使用math.pi和角度到弧度的公式来把角度转换成弧度。
"""
from math import pi


def degrees_to_rads(deg):
    return (deg * pi) / 180.0


# Examples

print(degrees_to_rads(180))
# output:
# ~3.1416（约等于）
