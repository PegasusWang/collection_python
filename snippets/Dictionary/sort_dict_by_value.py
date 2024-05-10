#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：按值对给定字典进行排序。

解读：
使用dict.items()从d获得一个元组对列表，并使用lambda函数和sorted()对其进行排序。
使用dict()将排序后的列表转换回字典。
使用sorted()中的reverse参数根据第二个参数对字典进行反向排序。
⚠️注意:字典值必须是相同的类型。
"""


def sort_dict_by_value(d, reverse=False):
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=reverse))


# Examples

d = {'one': 1, 'three': 3, 'five': 5, 'two': 2, 'four': 4}
print(sort_dict_by_value(d))
print(sort_dict_by_value(d, True))
# output:
# {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
# {'five': 5, 'four': 4, 'three': 3, 'two': 2, 'one': 1}
