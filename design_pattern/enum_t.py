#!/usr/bin/env python
# -*- coding:utf-8 -*-

# http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
# python <3.4 pip install enum34

from enum import Enum, IntEnum

'''
def enum(**kwargs):
    return type('Enum', (), kwargs)


Type = enum(
    a=1,
    b=2
)

#class MyEnum(object):
#    def __new__(cls):
#        members = [attr for attr in dir(Example()) if not callable(attr) and not attr.startswith("__")]
'''
