#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：创建开始(包括)和结束(不包括)之间的日期列表。

解读：
使用datetime.timedelta。从开始到结束的天数。
使用int()将结果转换为整数，使用range()迭代每一天。
使用列表推导式和datetime.timedelta()创建一个datetime.date对象列表。
"""
from datetime import timedelta, date


def daterange(start, end):
    return [start + timedelta(n) for n in range(int((end - start).days))]


# Examples

print(daterange(date(2020, 10, 1), date(2020, 10, 5)))
# output:
# [datetime.date(2020, 10, 1), datetime.date(2020, 10, 2), datetime.date(2020, 10, 3), datetime.date(2020, 10, 4)]
