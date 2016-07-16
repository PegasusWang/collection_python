#!/usr/bin/env python
# -*- coding:utf-8 -*-

# pip install cchardet
try:
    import cchardet
except ImportError:
    import chardet as cchardet

import requests


def get_encoding(data):
    return cchardet.detect(data)['encoding']


def convert_encoding(data, new_coding='UTF-8'):
    """未知编码转成utf8"""
    encoding = cchardet.detect(data)['encoding']
    if new_coding.upper() != encoding.upper():
        data = data.decode(encoding, data).encode(new_coding)
    return data


def to_unicode(unknown_bytes):
    encoding = cchardet.detect(unknown_bytes)['encoding']
    return unknown_bytes.decode(encoding)


def detect_html_encoding(url):
    r = requests.get(url).content
    return cchardet.detect(data)['encoding']



url = 'http://www.jb51.net/article/47995.htm'
r = requests.get(url)
print(r.encoding)
print(r.apparent_encoding)
print(get_encoding(r.content))
