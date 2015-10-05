#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tornado import gen, httpclient, ioloop
import time
from requests import get

class SynSpider(object):
    def __init__(self, urls):
        self.urls = urls

    def fetch_url(self, url):
        r = get(url)
        return r.content

    def handle_page(self, html):
        print html

    def run(self):
        for url in urls:
            html = self.fetch_url(url)
            self.handle_page(html)

class AsyncSpider(object):
    def __init__(self, urls):
        self.urls = urls

    @gen.coroutine
    def fetch_url(self, url):
        try:
            response = yield httpclient.AsyncHTTPClient().fetch(url)
        except:
            print 'fetch fail'
            raise gen.Return('')

        raise gen.Return(response.body)

    def handle_page(self, url, html):
        print url, html

    @gen.coroutine
    def _run(self):
        for url in self.urls:
            html = yield self.fetch_url(url)
            self.handle_page(url, html)

    def run(self):
        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self._run)


if __name__ == '__main__':
    urls = ['http://www.baidu.com'] * 100
    #urls = ['http://127.0.0.1:8000/'] * 20

    _st1 = time.time()
    s = AsyncSpider(urls)
    s.run()
    _end1 = time.time()

    _st2 = time.time()
    s2 = SynSpider(urls)
    s2.run()
    _end2 = time.time()

    print _end1 - _st1
    print _end2 - _st2

