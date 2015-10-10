#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from multiprocessing import Pool
from datetime import timedelta
from tornado import httpclient, gen, ioloop, queues


class AsySpider(object):
    """A simple class of asynchronous spider."""
    def __init__(self, urls, concurrency):
        urls.reverse()
        self.urls = urls
        self.concurrency = concurrency
        self._q = queues.Queue()
        self._fetching = set()
        self._fetched = set()

    def handle_page(self, url, html):
        #print(url, html)
        print(url)

    @gen.coroutine
    def get_page(self, url):
        try:
            response = yield httpclient.AsyncHTTPClient().fetch(url)
            print('######fetched %s' % url)
        except Exception as e:
            print('Exception: %s %s' % (e, url))
            raise gen.Return('')
        raise gen.Return(response.body)

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
                html = yield self.get_page(current_url)
                self._fetched.add(current_url)

                self.handle_page(current_url, html)

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
        assert self._fetching == self._fetched

    def run(self):
        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self._run)


def run_spider(beg, end):
    urls = []
    for page in range(beg, end):
        urls.append('http://www.jb51.net/article/%s.htm' % page)
    s = AsySpider(urls, 10)
    s.run()


def main():
    p = Pool()
    page_list = [(1, 20), (21, 30), (31, 40), (41, 50)]
    for i in page_list:
        p.apply_async(run_spider, args=(i[0], i[1],))
    p.close()
    p.join()


if __name__ == '__main__':
    main()
