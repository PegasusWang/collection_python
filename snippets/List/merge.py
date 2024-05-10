#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将两个或多个列表合并为列表的列表，根据每个输入列表的位置组合元素。

解读：
使用max()与列表推导式结合使用来获取参数中最长列表的长度。
将range()与max_length变量结合使用，只要最长列表中有元素，就可以循环多次。
如果列表小于max_length，剩余的项使用fill_value(默认为None)。
zip()和itertools.zip_longest()提供了与此代码片段类似的功能。
"""


def merge(*args, fill_value=None):
    max_length = max(len(lst) for lst in args)
    return [
        [
            args[k][i] if i < len(args[k]) else fill_value
            for k in range(len(args))
        ]
        for i in range(max_length)
    ]


# Examples

print(merge(['a', 'b'], [1, 2], [True, False]))
print(merge(['a'], [1, 2], [True, False]))
print(merge(['a'], [1, 2], [True, False], fill_value='_'))
# output:
# [['a', 1, True], ['b', 2, False]]
# [['a', 1, True], [None, 2, False]]
# [['a', 1, True], ['_', 2, False]]
