#!/usr/bin/env python
# -*- coding:utf-8 -*-


try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


def get_query_dict(url):
    return dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
