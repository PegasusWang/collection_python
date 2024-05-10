#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：按键对给定字典进行排序。

解读：
使用dict.items()从d获得一个元组对列表，并使用sorted()对其进行排序。
使用dict()将排序后的列表转换回字典。
使用sorted()中的reverse参数根据第二个参数对字典进行反向排序。
"""


def sort_dict_by_key(d, reverse=False):
    return dict(sorted(d.items(), reverse=reverse))


# Examples

d = {'one': 1, 'three': 3, 'five': 5, 'two': 2, 'four': 4}
print(sort_dict_by_key(d))
print(sort_dict_by_key(d, True))
# output:
# {'five': 5, 'four': 4, 'one': 1, 'three': 3, 'two': 2}
# {'two': 2, 'three': 3, 'one': 1, 'four': 4, 'five': 5}
