#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将字符串转换为snake case。

解读：
使用re.sub()匹配字符串中的所有单词，str.lower()将它们小写。
使用re.sub()将任意-字符替换为空格。
最后，使用str.join()以-作为分隔符组合所有单词。
"""
from re import sub


def snake(s):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


# Examples

print(snake('camelCase'))
print(snake('some text'))
print(snake('some-mixed_string With spaces_underscores-and-hyphens'))
print(snake('AllThe-small Things'))
# output:
# camel_case
# some_text
# some_mixed_string_with_spaces_underscores_and_hyphens
# all_the_small_things
