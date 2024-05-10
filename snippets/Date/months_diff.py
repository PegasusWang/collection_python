#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：计算两个日期之间的月差。

解读：
从end减去start，然后使用datetime.timedelta。得到日差。
除以30，并使用math.ceil()得到以月为单位的差值(取整)。
"""
from math import ceil


def months_diff(start, end):
    return ceil((end - start).days / 30)


# Examples

from datetime import date

print(months_diff(date(2020, 10, 28), date(2020, 11, 25)))
# output:
# 1
