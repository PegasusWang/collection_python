#!/usr/bin/env python
# -*- coding:utf-8 -*-

# py2
from urllib import urlencode, quote, unquote

# py3
#from urllib.parse import urlparse, quote, urlencode, unquote
data = {
    'a': u'中文',
    'b': 2
}

print urlencode(data)    # 对dict encode
s = '呵呵'
print quote(s)    # 对字符串encode

print unquote(urlencode(data))
print unquote(s)
