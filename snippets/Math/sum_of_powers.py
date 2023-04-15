#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：返回从开始到结束（包括两端）的所有数字的幂的和。

解读：
将range()与列表推导式结合使用，创建一个指定范围内的元素列表
使用sum()将这些值相加。
忽略第二个参数power，使用默认的2的幂。
忽略第三个参数start，使用默认的起始值1。
"""


def sum_of_powers(end, power=2, start=1) -> int:
    return sum((i) ** power for i in range(start, end + 1))


# Examples

print(sum_of_powers(10))
print(sum_of_powers(10, 3))
print(sum_of_powers(10, 3, 5))
# output:
# 385
# 3025
# 2925
