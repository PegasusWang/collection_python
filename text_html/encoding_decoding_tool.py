#!/usr/bin/env python
# -*- coding:utf-8 -*-

# pip install cchardet
try:
    import cchardet as chardet
except ImportError:
    import chardet
import requests


def get_encoding(unknown_bytes):
    return chardet.detect(unknown_bytes)['encoding']


def convert_encoding(data, new_coding='UTF-8'):
    """未知编码转成utf8"""
    encoding = chardet.detect(data)['encoding']
    if new_coding.upper() != encoding.upper():
        data = data.decode(encoding, data).encode(new_coding)
    return data


def to_unicode(unknown_bytes):
    encoding = chardet.detect(unknown_bytes)['encoding']
    return unknown_bytes.decode(encoding)


def detect_html_encoding(url):
    data = requests.get(url).content
    return chardet.detect(data)['encoding']


if __name__ == '__main__':
    print detect_html_encoding('http://www.baidu.com')
    convert_encoding('hehe', new_coding='UTF-8')
    to_unicode('hehe')
    print get_encoding('hehe')
