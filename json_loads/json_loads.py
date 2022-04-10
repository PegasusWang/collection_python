#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
How to get string objects instead of Unicode from JSON?
Updated for Python 2.7 and 3.x compatibility.
https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-from-json/33571117#33571117
"""
import json


def json_load_byteified(file_handle):
    """
    It converts all unicode strings in a JSON object to UTF-8 encoded strings
    
    :param file_handle: The file handle to the JSON file that you want to load
    """
    return _byteify(json.load(file_handle, object_hook=_byteify), ignore_dicts=True)


def json_loads_byteified(json_text):
    """
    It converts all unicode strings in a JSON object to UTF-8 encoded strings
    
    :param json_text: The JSON string that you want to convert to a Python object
    """
    return _byteify(json.loads(json_text, object_hook=_byteify), ignore_dicts=True)


def _byteify(data, ignore_dicts=False):
    """
    It converts all unicode strings in a data structure to UTF-8 encoded strings
    
    :param data: the data to be converted
    :param ignore_dicts: If this is True, then dictionaries are ignored, defaults to False (optional)
    """
    if isinstance(data, str):
        return data

    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items()  # changed to .items() for python 2.7/3
        }

    # python 3 compatible duck-typing
    # if this is a unicode string, return its string representation
    if str(type(data)) == "<type 'unicode'>":
        return data.encode('utf-8')

    # if it's anything else, return it in its original form
    return data


if __name__ == '__main__':
    # Example usage:
    print(json_loads_byteified('{"Hello": "World"}'))
    # {'Hello': 'World'}
    print(json_loads_byteified('"I am a top-level string"'))
    # 'I am a top-level string'
    print(json_loads_byteified('7'))
    # 7
    print(json_loads_byteified('["I am inside a list"]'))
    # ['I am inside a list']
    print(json_loads_byteified('[[[[[[[["I am inside a big nest of lists"]]]]]]]]'))
    # [[[[[[[['I am inside a big nest of lists']]]]]]]]
    print(json_loads_byteified('{"foo": "bar", "things": [7, {"qux": "baz", "moo": {"cow": ["milk"]}}]}'))
    # {'things': [7, {'qux': 'baz', 'moo': {'cow': ['milk']}}], 'foo': 'bar'}
    print(json_load_byteified(open('somefile.json', encoding='utf-8')))
    # {'more json': 'from a file'}
