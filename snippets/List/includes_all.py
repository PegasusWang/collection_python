#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：检查值中的所有元素是否都包含在lst中

解读：
使用for循环检查value中的每个值是否都包含在lst中。
如果找不到任何一个值则返回False，否则返回True。
"""


def includes_all(lst, values):
    return all(v in lst for v in values)


# Examples

print(includes_all([1, 2, 3, 4], [1, 4]))
print(includes_all([1, 2, 3, 4], [1, 5]))
# output:
# True
# False
