#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将字符串转换为url友好的字符串。

解读:
使用str.lower()和str.strip()来规范化输入字符串。
使用re.sub()来替换空格、破折号和下划线，并删除特殊字符。
"""
import re


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s


# Examples

print(slugify('Hello World!'))
# output:
# hello-world
