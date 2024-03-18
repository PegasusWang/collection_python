#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：反转具有唯一可哈希值的字典。

解读：
结合列表理解使用dictionary.items()创建一个值和键反向的新字典。
"""


def invert_dictionary(obj):
    return {value: key for key, value in obj.items()}


# Examples

ages = {
    'Peter': 10,
    'Isabel': 11,
    'Anna': 9,
}
print(invert_dictionary(ages))
# output:
# { 10: 'Peter', 11: 'Isabel', 9: 'Anna' }
