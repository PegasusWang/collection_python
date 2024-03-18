#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将一个字符串转换为烤肉串大小写。

解读：
使用re.sub()将任何-或_替换为一个空格，使用regexp r"(_|-)+"。
使用re.sub()匹配字符串中的所有单词，str.lower()将它们小写。
最后，使用str.join()以-作为分隔符组合所有单词。
"""
from re import sub


def kebab(s):
    return '-'.join(
        sub(
            r"(\s|_|-)+",
            " ",
            sub(
                r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
                lambda mo: f' {mo.group(0).lower()}',
                s,
            ),
        ).split()
    )


# Examples

print(kebab('camelCase'))
print(kebab('some text'))
print(kebab('some-mixed_string With spaces_underscores-and-hyphens'))
print(kebab('AllThe-small Things'))
# output:
# camel-case
# some-text
# some-mixed-string-with-spaces-underscores-and-hyphens
# all-the-small-things
