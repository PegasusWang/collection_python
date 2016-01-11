#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Singleton1(object):
    """实现方式1：使用__new__"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton1, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


class Singleton2(object):
    """创建实例把所有实例的__dict__都指向同一个字典，使具有相同的属性和方法
    伪单例
    """
    _state = {}

    def __new__(cls, *args, **kwargs):
        ob = super(Singleton2, cls).__new__(cls, *args, **kwargs)
        ob.__dict__ = cls._state
        return ob


def Singleton3(cls, *args, **kwargs):
    """装饰器版本的单例"""
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance


@Singleton3
class Singleton(object):
    pass


'''
# 方法4：作为python的模块是天然的单例模式
# mysingleton.py
class My_Singleton(object):
    def foo(self):
        pass

my_singleton = My_Singleton()

# to use
from mysingleton import my_singleton

my_singleton.foo()
'''


def test_singleton():
    """use py.test for unit test"""
    s1 = Singleton()
    s2 = Singleton()
    assert id(s1) == id(s2)
    assert s1 is s2
