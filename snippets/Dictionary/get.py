#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：从字典或列表中检索给定选择器列表指示的嵌套键的值。

解读：
使用functools.reduce()遍历选择器列表。
对选择器中的每个键应用operator.getitem()，检索将用于下一次迭代的迭代对象的值。
"""

from functools import reduce
from operator import getitem


def get(d, selectors):
    return reduce(getitem, selectors, d)


# Examples

users = {
    'freddy': {
        'name': {
            'first': 'fred',
            'last': 'smith'
        },
        'postIds': [1, 2, 3]
    }
}
print(get(users, ['freddy', 'name', 'last']))
print(get(users, ['freddy', 'postIds', 1]))
# output:
# smith
# 2
