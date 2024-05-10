#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：从其ISO-8601表示形式转换日期。

解读：
使用datetime.datetime.fromisoformat()将给定的ISO-8601日期转换为datetime.datetime对象。
"""
from datetime import datetime


def from_iso_date(d):
    return datetime.fromisoformat(d)


# Examples

print(from_iso_date('2020-10-28T12:30:59.000000'))
# output:
# 2020-10-28 12:30:59
