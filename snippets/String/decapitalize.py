#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将字符串的首字母大写。

解读：
使用列表切片和str.lower()对字符串的第一个字母大写。
使用str.join()将小写的第一个字母与其余字符组合在一起。
省略upper_rest参数以保持字符串的其余部分不变，或将其设置为True以转换为大写字母。
"""


def decapitalize(s, upper_rest=False):
    return ''.join([s[:1].lower(), (s[1:].upper() if upper_rest else s[1:])])


# Examples

print(decapitalize('FooBar'))
print(decapitalize('FooBar', True))
# output:
# fooBar
# fOOBAR
