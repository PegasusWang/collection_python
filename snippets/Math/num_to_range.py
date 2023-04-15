#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将数字从一个范围映射到另一范围。

解读：
从inMin-inMax返回outMin-outMax之间的映射num。
"""


def num_to_range(num, inMin, inMax, outMin, outMax):
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))


# Examples

print(num_to_range(5, 0, 10, 0, 100))
# output:
# 50.0
