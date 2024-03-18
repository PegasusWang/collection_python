#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将一个字符串转换为驼峰大小写。

解读：
使用re.sub()将任何-或_替换为一个空格，使用regexp r"(_|-)+"。
使用str.title()将每个单词的第一个字母大写，并将其余的转换为小写。
最后，使用str.replace()删除单词之间的空格。
"""
from re import sub


def camel(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])


# Examples

print(camel('some_database_field_name'))
print(camel('Some label that needs to be camelized'))
print(camel('some-javascript-property'))
print(camel('some-mixed_string with spaces_underscores-and-hyphens'))
# output:
# someDatabaseFieldName
# someLabelThatNeedsToBeCamelized
# someJavascriptProperty
# someMixedStringWithSpacesUnderscoresAndHyphens
