#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将日期转换为其ISO-8601表示形式。

解读：
使用datetime.datetime.isoformat()转换给定的datetime.datetime对象设置为ISO-8601日期。
"""
from datetime import datetime


def to_iso_date(d):
    return d.isoformat()


# Examples

print(to_iso_date(datetime(2020, 10, 25)))
# output:
# 2020-10-25T00:00:00
