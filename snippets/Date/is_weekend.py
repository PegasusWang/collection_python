#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查给定日期是否为周末。

解读：
使用datetime.datetime.weekday()以整数形式获取星期几。
检查一周中的一天是否大于4。
忽略第二个参数d，使用datetime.today()的默认值。
"""
from datetime import datetime


def is_weekend(d = datetime.now()):
    return d.weekday() > 4


# Examples

from datetime import date

print(is_weekend(date(2020, 10, 25)))
print(is_weekend(date(2020, 10, 28)))
# output:
# True
# False