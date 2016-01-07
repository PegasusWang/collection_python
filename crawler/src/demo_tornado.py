#!/usr/bin/env python
# -*- coding:utf-8 -*-


from datetime import timedelta
from bs4 import BeautifulSoup
from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop, gen, queues


@gen.coroutine
def fetch(url):
    print('fetcing', url)
    response = yield AsyncHTTPClient().fetch(url, raise_error=False)
    raise gen.Return(response)

_q = queues.Queue()


@gen.coroutine
def run():
    try:
        url = yield _q.get()
        res = yield fetch(url)
        html = res.body
        soup = BeautifulSoup(html)
        print(str(soup.find('title')))
    finally:
        _q.task_done()


@gen.coroutine
def worker():
    while True:
        yield run()


@gen.coroutine
def main():
    for i in range(1, 1000):
        #url = "http://tech2ipo.com/10026522.html"
        url = "http://pyhome.org/about/"
        _q.put(url)
    for _ in range(1000):
        worker()
    yield _q.join(timeout=timedelta(seconds=30))


if __name__ == '__main__':
    ioloop.IOLoop.current().run_sync(main)
