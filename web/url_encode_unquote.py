#!/usr/bin/env python
# -*- coding:utf-8 -*-

try:
    from urllib import urlencode, quote, unquote  # py2
except ImportError:
    from urllib.parse import urlparse, quote, urlencode, unquote  # py3

# py3
data = {
    'a': u'中文',
    'b': 2
}

print urlencode(data)    # 对dict encode
s = '呵呵'
print quote(s)    # 对字符串encode

print unquote(urlencode(data))
print unquote(s)

# tornado send post
post_data = { 'data': 'test data' } #A dictionary of your post data
body = urlencode(post_data) #Make it into a post request
http_client.fetch("http://0.0.0.0:8888", handle_request, method='POST', headers=None, body=body) #Send it off!
