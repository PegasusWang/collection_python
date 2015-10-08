#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tornado import gen, httpclient, ioloop
import time
from requests import get


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
        filename = url.rsplit('/')[1]
        print('save filename')
        with open(filename, 'w+') as f:
            f.write(html)

    @gen.coroutine
    def _run(self):
        for url in self.urls:
            html = yield self.fetch_url(url)
            self.handle_page(url, html)

    def run(self):
        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self._run)


if __name__ == '__main__':
    urls = []
    for page in range(1, 73000):
        urls.append('http://www.jb51.net/article/%s.htm' % page)

    s = AsyncSpider(urls)
    s.run()
