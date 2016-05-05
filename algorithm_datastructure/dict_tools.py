#!/usr/bin/env python
# -*- coding:utf-8 -*-


class ObjectDict(dict):
    """from tornado.util.ObjectDict, access dict by dot"""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


import collections


class TransformedDict(collections.MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

# pip install fronzendict

class FronzenDict(TransformedDict):
    """immutable dict, init by a dict"""
    def __init__(self, d):
        self.store = d

    def __setitem__(self, key, value):
        # self.store[self.__keytransform__(key)] = value
        raise TypeError("'FronzenDict' object does not support item assignment")


# since python3.3, you can use immutable dict
import types
d_proxy = types.MappingProxyType(d)    # can add new key/value by assignment but can not assign key alrady exists
