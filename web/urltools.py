#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


def get_query_dict(url):
    return dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))


def is_valid_url(url):
    """http://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python"""
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url is not None and regex.search(url))

if __name__ == "__main__":
    print(is_valid_url(None))
    print(is_valid_url(''))
    print(is_valid_url('http://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python'))
    print(is_valid_url('https://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python'))
