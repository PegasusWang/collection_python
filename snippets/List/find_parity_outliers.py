#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：查找给定列表中奇偶校验异常值的项。

解读：
使用集合。使用列表推导式计算列表中的偶数和奇数值。
使用collections.Counter.most_common()来获得最常见的奇偶校验。
使用列表推导式查找所有不匹配最常见奇偶校验的元素。
"""
from collections import Counter


def find_parity_outliers(nums):
    return [
        x for x in nums
        if x % 2 != Counter([n % 2 for n in nums]).most_common()[0][0]
    ]


# Examples

print(find_parity_outliers([1, 2, 3, 4, 6]))
# output:
# [1, 3]
