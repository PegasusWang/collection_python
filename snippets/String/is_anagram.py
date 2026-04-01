#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查一个字符串是否是另一个字符串的变形词(不区分大小写，忽略空格、标点和特殊字符)。

解读:
使用str.isalnum()过滤出非字母数字字符，使用str.lower()将每个字符转换为小写字母。
使用集合。计数器计算每个字符串的结果字符并比较结果。
"""
from collections import Counter


def is_anagram(s1, s2):
    return Counter(
        c.lower() for c in s1 if c.isalnum()
    ) == Counter(
        c.lower() for c in s2 if c.isalnum()
    )


# Examples

print(is_anagram('#anagram', 'Nag a ram!'))
# output:
# True
