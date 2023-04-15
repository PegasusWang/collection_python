#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
功能实现：计算给定日期后n天的日期。

解读：
使用datetime.timedelta和+运算符来计算新datetime.datetime在d中添加n天后的值。
忽略第二个参数d，使用datetime.today()的默认值
"""
from datetime import datetime, timedelta, date


def add_days(n, d = datetime.now()):
    return d + timedelta(n)


# Examples

print(add_days(5, date(2020, 10, 25)))
print(add_days(-5, date(2020, 10, 25)))
# output:
# 2020-10-30
# 2020-10-20
