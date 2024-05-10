#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将多行字符串拆分为行列表。

解读:
使用str.split()和'\n'来匹配换行符并创建列表。
str.splitlines()提供了与此代码片段类似的功能。
"""


def split_lines(s):
    return s.split('\n')


# Examples

print(split_lines('This\nis a\nmultiline\nstring.\n'))
# output:
# ['This', 'is a', 'multiline', 'string.' , '']
