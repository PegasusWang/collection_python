#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将num限制在边界值指定的范围之内。

解读：
如果num在(a, b)范围内，返回num。
否则，返回范围内最近的数字。
"""


def clamp_number(num, a, b):
    return max(min(num, max(a, b)), min(a, b))


# Examples

print(clamp_number(2, 3, 5))
print(clamp_number(1, -1, -5))
# output:
# 3
# -1
