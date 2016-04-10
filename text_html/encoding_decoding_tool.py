#!/usr/bin/env python
# -*- coding:utf-8 -*-

# pip install cchardet
import cchardet


def get_encoding(data):
    return cchardet.detect(data)['encoding']


def convert_encoding(data, new_coding='UTF-8'):
    """未知编码转成utf8"""
    encoding = cchardet.detect(data)['encoding']
    if new_coding.upper() != encoding.upper():
        data = data.decode(encoding, data).encode(new_coding)
    return data
