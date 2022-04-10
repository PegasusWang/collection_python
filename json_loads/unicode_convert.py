#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
解决Python 2下的json.loads()导致的unicode编码问题
"""
from __future__ import print_function

import json


def unicode_convert(data):
    """
    A recursive function that converts all unicode strings in a dictionary to utf-8 encoded strings.
    :param data: The unicode string to be converted
    """
    if isinstance(data, dict):
        return {unicode_convert(key): unicode_convert(value) for key, value in data.items()}
    if isinstance(data, list):
        return [unicode_convert(element) for element in data]
    return data.encode('utf-8') if str(type(data)) == "<type 'unicode'>" else data


json_text = json.dumps({'dns': None, 'ntp': None})
print('json_text:', json_text)
dict_value = json.loads(json_text)
print(unicode_convert(dict_value))

datas = {"foo": "bar", "things": [7, {"qux": "baz", "moo": {"cow": ["milk"]}}]}
json_text2 = json.dumps(datas)
print('json_text2:', json_text2)
dict_value2 = json.loads(json_text2)
print('dict_value:', dict_value2)
print(unicode_convert(dict_value2))

print(unicode_convert(json.loads('{"foo": "bar", "things":"apple"}')))

print(unicode_convert(json.loads('{"foo": "bar"}')))

# python3 output:
# json_text: {"dns": null, "ntp": null}
# {'dns': None, 'ntp': None}
# json_text2: {"foo": "bar", "things": [7, {"qux": "baz", "moo": {"cow": ["milk"]}}]}
# dict_value: {'foo': 'bar', 'things': [7, {'qux': 'baz', 'moo': {'cow': ['milk']}}]}
# {'foo': 'bar', 'things': [7, {'qux': 'baz', 'moo': {'cow': ['milk']}}]}
# {'foo': 'bar', 'things': 'apple'}
# {'foo': 'bar'}

# python2 output:
# json_text: {"ntp": null, "dns": null}
# {'ntp': None, 'dns': None}
# json_text2: {"things": [7, {"qux": "baz", "moo": {"cow": ["milk"]}}], "foo": "bar"}
# dict_value: {u'things': [7, {u'qux': u'baz', u'moo': {u'cow': [u'milk']}}], u'foo': u'bar'}
# {'things': [7, {'qux': 'baz', 'moo': {'cow': ['milk']}}], 'foo': 'bar'}
# {'things': 'apple', 'foo': 'bar'}
# {'foo': 'bar'}