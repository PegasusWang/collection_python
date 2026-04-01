#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：计算从今天算起n天前的日期。

解读：
使用datetime.date.today()获取当前日期。
使用datetime.timedelta从今天的日期减去n天。
"""
from datetime import timedelta, date


def days_ago(n):
    return date.today() - timedelta(n)


# Examples

print(days_ago(5))
# output:
# 2021-03-28
