#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将字符串的第一个字母大写。

解读：
使用列表切片和str.upper()将字符串的第一个字母大写。
使用str.join()将大写的第一个字母与其他字符组合起来。
省略lower_rest参数以保持字符串的其余部分完整，或将其设置为True以转换为小写。
"""


def capitalize(s, lower_rest=False):
    return ''.join([s[:1].upper(), (s[1:].lower() if lower_rest else s[1:])])


# Examples

print(capitalize('fooBar'))
print(capitalize('fooBar', True))
# output:
# FooBar
# Foobar
