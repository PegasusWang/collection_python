#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将给定的字符串转换为单词列表。

解读：
使用re.findall()与提供的模式一起查找所有匹配的子字符串。
省略第二个参数以使用默认regexp，它匹配字母数字和连字符。
"""
import re


def words(s, pattern='[a-zA-Z-]+'):
    return re.findall(pattern, s)


# Examples

print(words('I love Python!!'))
print(words('python, javaScript & coffee'))
print(words('build -q --out one-item', r'\b[a-zA-Z-]+\b'))
# output:
# ['I', 'love', 'Python']
# ['python', 'javaScript', 'coffee']
# ['build', 'q', 'out', 'one-item']
