#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能实现：创建一个函数，该函数将为给定对象上的指定属性调用谓词函数。

解读：
返回一个lambda函数，该函数接受一个对象并将谓词函数fn应用到指定的属性。
"""


def check_prop(fn, prop):
    return lambda obj: fn(obj[prop])


# Examples

check_age = check_prop(lambda x: x >= 18, 'age')
user = {'name': 'Mark', 'age': 18}
print(check_age(user))
# output:
# True
