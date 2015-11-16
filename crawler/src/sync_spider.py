#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from datetime import timedelta
import traceback
from extract import extract
from requests import get


class SyncSpider(object):
    def __init__(self, urls):
        self.urls = urls

    def fetch(self, url, **kwargs):
        return get(url, **kwargs)

    def handle_html(self, url, html):
        raise NotImplementedError

    def handle_response(self, url, response):
        if response.status_code == 200:
            self.handle_html(url, response.content)

    def run(self):
        for url in self.urls:
            response = self.fetch(url)
            self.handle_response(url, response)


def main():
    st = time.time()
    urls = []
    for page in range(1, 1000):
        urls.append('http://www.jb51.net/article/%s.htm' % page)
    s = MySpider(urls)
    s.run()
    print(time.time()-st)


if __name__ == '__main__':
    main()
