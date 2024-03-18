#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查所提供的函数是否对列表中的每个元素都返回True。

解读：
将all()与map()和fn结合使用，检查fn是否为列表中的所有元素返回True。
"""


def every(lst, fn=lambda x: x):
    return all(map(fn, lst))


# Examples

print(every([4, 2, 3], lambda x: x > 1))
print(every([1, 2, 3]))
# output:
# True
# True
