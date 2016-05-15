#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from extract import *
from async_spider import AsyncSpider
from sync_spider import SyncSpider


class TestSyncSpider(SyncSpider):
    def handle_html(self, url, html):
        print(html)
        pass


class TestAsyncSpider(AsyncSpider):
    def handle_html(self, url, html):
        print(html)
        pass


urls = []
for page in range(1, 1000):
    #urls.append('http://www.jb51.net/article/%s.htm' % page)
    urls.append('http://www.imooc.com/data/check_f.php?page=%d'%page)


def test_async():
    st1 = time.time()
    s1 = TestAsyncSpider(urls)
    s1.run()
    end1 = time.time()-st1
    print('ASync', end1)


def test_sync():
    st2 = time.time()
    s2 = TestSyncSpider(urls)
    s2.run()
    end2 = time.time()-st2
    print('Sync', end2)


if __name__ == '__main__':
    #test_sync()
    test_async()
