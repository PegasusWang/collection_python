#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将角度从弧度转换为角度。

解读：
使用math.pi和弧度到度数的公式将角度从弧度转换成角度。
"""
from math import pi


def rads_to_degrees(rad):
    return (rad * 180.0) / pi


# Examples

print(rads_to_degrees(pi / 2))
# output:
# 90.0
