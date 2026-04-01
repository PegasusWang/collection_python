#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查value中的任何元素是否包含在lst中。

解读：
使用for循环检查values中的任何值是否包含在lst中。
如果找到任何一个值则返回True，否则返回False。
"""


def includes_any(lst, values):
    return any(v in lst for v in values)


# Examples

print(includes_any([1, 2, 3, 4], [2, 9]))
print(includes_any([1, 2, 3, 4], [8, 9]))
# output:
# True
# False
