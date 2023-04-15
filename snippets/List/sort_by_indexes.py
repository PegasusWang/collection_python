#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：根据包含所需索引的另一个列表对一个列表进行排序。

解读：
使用zip()和sorted()根据索引的值组合并排序这两个列表。
使用列表推导式从结果中获取每对元素的第一个元素。
使用sorted()中的reverse参数根据第三个参数对字典进行反向排序。
"""


def sort_by_indexes(lst, indexes, reverse=False):
    return [val for (_, val) in sorted(zip(indexes, lst), key=lambda x: x[0], reverse=reverse)]


# Examples

a = ['eggs', 'bread', 'oranges', 'jam', 'apples', 'milk']
b = [3, 2, 6, 4, 1, 5]
print(sort_by_indexes(a, b))
print(sort_by_indexes(a, b, True))
# output:
# ['apples', 'bread', 'eggs', 'jam', 'milk', 'oranges']
# ['oranges', 'milk', 'jam', 'eggs', 'bread', 'apples']
