#!/usr/bin/env python
# -*- coding:utf-8 -*-
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


def to_value(cls):
    # members = {
        # attr: getattr(cls, attr).value
        # for attr in dir(cls) if not callable(attr) and
        # not attr.startswith("__")
    # }
    #print(type(getattr(cls, 'a')))
    value = getattr(cls, 'a').value
    setattr(cls, 'a', value)
    return cls


@to_value
class T(Enum):
    a = 1
    b = 2


print(T.a)
#print(type(T.a))
