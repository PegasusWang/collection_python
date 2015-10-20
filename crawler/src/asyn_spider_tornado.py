#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from datetime import timedelta
from tornado import httpclient, gen, ioloop, queues
import traceback


class AsySpider(object):
    """A simple class of asynchronous spider."""
    def __init__(self, urls, concurrency=10, **params):
        urls.reverse()
        self.urls = urls
        self.concurrency = concurrency
        self._q = queues.Queue()
        self._fetching = set()
        self._fetched = set()
        self.params = params

    def handle_page(self, url, html):
        """inherit and rewrite this method"""
        #print(url, html)
        print(html)

    @gen.coroutine
    def get_page(self, url, **kwargs):
        try:
            response = yield httpclient.AsyncHTTPClient().fetch(url, **kwargs)
            print('######fetched %s' % url)
        except Exception as e:
            print('Exception: %s %s' % (e, url))
            raise gen.Return(e)
        raise gen.Return(response)

    @gen.coroutine
    def _run(self):

        @gen.coroutine
        def fetch_url():
            current_url = yield self._q.get()
            try:
                if current_url in self._fetching:
                    return

                print('fetching****** %s' % current_url)
                self._fetching.add(current_url)
                response = yield self.get_page(current_url, **self.params)
                if response.code == 200:
                    self.handle_page(current_url, response.body)
                self._fetched.add(current_url)

                if response.code == 599:    # timeout or empty response
                    self._fetching.remove(current_url)
                    yield self._q.put(current_url)    # retry if timeout

                for i in range(self.concurrency):
                    if self.urls:
                        yield self._q.put(self.urls.pop())

            finally:
                self._q.task_done()

        @gen.coroutine
        def worker():
            while True:
                yield fetch_url()

        self._q.put(self.urls.pop())

        # Start workers, then wait for the work queue to be empty.
        for _ in range(self.concurrency):
            worker()
        yield self._q.join(timeout=timedelta(seconds=300000))
        print self._fetching - self._fetched
        print self._fetched - self._fetching
        assert self._fetching == self._fetched

    def run(self):
        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self._run)


def main():
    urls = []
    for page in range(47995, 47996):
        urls.append('http://www.jb51.net/article/%s.htm' % page)

    headers = {
        'User-Agent': 'mozilla/5.0 (compatible; baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    }
    s = AsySpider(urls, 10, headers=headers)
    s.run()

if __name__ == '__main__':
    main()
