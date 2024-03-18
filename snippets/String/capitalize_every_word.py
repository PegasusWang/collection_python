#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将字符串中每个单词的首字母大写。

解读:
使用str.title()将字符串中每个单词的第一个字母大写。
"""


def capitalize_every_word(s) -> str:
    return s.title()


# Examples

print(capitalize_every_word('hello world!'))
# output:
# 'Hello World!'
