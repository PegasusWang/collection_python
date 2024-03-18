#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：通过将列表中的元素扩展到一个新的列表中，使列表变平。

解读：
循环遍历元素，如果元素是列表则使用list.extend()，否则使用list.append()。
"""


def spread(arg):
    ret = []
    for i in arg:
        ret.extend(i) if isinstance(i, list) else ret.append(i)
    return ret


# Examples

print(spread([1, 2, 3, [4, 5, 6], [7], 8, 9]))
# output:
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
