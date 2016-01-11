#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


class T(Singleton):
    pass


def test():
    s1 = T()
    s2 = T()
    assert s1 is s2
