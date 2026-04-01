#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：将两个列表组合到一个字典中，其中第一个列表的元素作为键，第二个列表的元素作为值。第一个列表的值必须是唯一的，并且是可哈希的。

解读：
将zip()与dict()结合使用，可以将两个列表的值组合到一个字典中。
"""


def to_dictionary(keys, values):
    return dict(zip(keys, values))


# Examples

print(to_dictionary(['a', 'b'], [1, 2]))
# output:
# { a: 1, b: 2 }
