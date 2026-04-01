#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查给定的字符串是否是回文。

解读:
使用str.lower()和re.sub()将其转换为小写，并从给定的字符串中删除非字母数字字符。
然后，使用切片表示法将新字符串与其相反的字符串进行比较。
"""
from re import sub


def palindrome(s) -> bool:
    s = sub('[\W_]', '', s.lower())
    return s == s[::-1]


# Examples

print(palindrome('taco cat'))
# output:
# True
