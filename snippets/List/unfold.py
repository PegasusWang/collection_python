#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：使用迭代器函数和初始种子值构建列表。

解读：
迭代器函数接受一个参数(seed)，并且必须总是返回一个包含两个元素的列表([value, nextSeed])，或者返回False以终止。
使用生成器函数fn_generator，它使用while循环调用迭代器函数并生成该值，直到它返回False。
使用列表推导式，使用迭代器函数返回生成器生成的列表。
"""


def unfold(fn, seed):
    def fn_generator(val):
        while True:
            val = fn(val[1])
            if val is False: break
            yield val[0]

    return list(fn_generator([None, seed]))


# Examples

f = lambda n: False if n > 50 else [-n, n + 10]
print(unfold(f, 10))
# output:
# [-10, -20, -30, -40, -50]
