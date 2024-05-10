#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：找到一组数字的中位数。

解读：
使用list.Sort()对列表中的数字进行排序。
找到中值，如果列表长度为奇数，它是列表的中间元素;如果列表长度为偶数，它是列表中间两个元素的平均值。
statistics.median()提供了与此代码片段类似的功能。
"""


def median(list):
    list.sort()
    list_length = len(list)
    if list_length % 2 == 0:
        return (list[list_length // 2 - 1] + list[list_length // 2]) / 2
    return float(list[list_length // 2])


# Examples

print(median([1, 2, 3]))
print(median([1, 2, 3, 4]))
# output:
# 2.0
# 2.5
