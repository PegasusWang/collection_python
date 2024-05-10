#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：计算两个日期之间的日差。

解读：
从end减去start，然后使用datetime.timedelta.days得到日差。
"""
from datetime import date


def days_diff(start, end):
    return (end - start).days


# Examples

print(days_diff(date(2020, 10, 25), date(2020, 10, 28)))
# output:
# 3