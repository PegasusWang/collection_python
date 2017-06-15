#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import logging
from datetime import timedelta
from tornado import httpclient, gen, ioloop, queues
import traceback
from bs4 import BeautifulSoup


def logged(class_):
    logging.basicConfig(level=logging.INFO)
    class_.logger = logging.getLogger(class_.__name__)
    return class_


@logged
class AsyncSpider(object):
    """A simple class of asynchronous spider."""
    def __init__(self, urls=None, concurrency=10, results=None,
                 sleep=None, **kwargs):
        super(AsyncSpider, self).__init__(**kwargs)

        self.concurrency = concurrency
        self._q = queues.Queue()
        self._fetching = set()
        self._fetched = set()
        self.sleep = sleep
        self.urls = urls or []
        if results is None:
            self.results = []
        if not self.urls:
            self.init_urls()
        for url in self.urls:
            self._q.put(url)
        httpclient.AsyncHTTPClient.configure(
            "tornado.curl_httpclient.CurlAsyncHTTPClient"
        )

    def init_urls(self):
        """init_urls generate urls to self.urls"""
        raise NotImplementedError

    def fetch(self, url, **kwargs):
        fetch = getattr(httpclient.AsyncHTTPClient(), 'fetch')
        http_request = httpclient.HTTPRequest(url, **kwargs)
        return fetch(http_request, raise_error=False)

    def handle_html(self, url, html):
        """处理html页面"""
        print(url)

    def handle_response(self, url, response):
        """处理http响应，对于200响应码直接处理html页面，
        否则按照需求处理不同响应码"""
        if response.code == 200:
            self.handle_html(url, response.body)

        elif response.code == 599:    # retry
            self._fetching.remove(url)
            self._q.put(url)

    @gen.coroutine
    def get_page(self, url):
        if self.sleep is not None:
            yield gen.sleep(self.sleep)    # sleep when need
        try:
            response = yield self.fetch(url)
            self.logger.debug('######fetched %s' % url)
        except Exception as e:
            self.logger.debug('Exception: %s %s' % (e, url))
            raise gen.Return(e)
        raise gen.Return(response)    # py3 can just return response

    @gen.coroutine
    def _run(self):
        @gen.coroutine
        def fetch_url():
            current_url = yield self._q.get()
            try:
                if current_url in self._fetching:
                    return

                self.logger.debug('fetching****** %s' % current_url)
                self._fetching.add(current_url)

                response = yield self.get_page(current_url)
                self.handle_response(current_url, response)    # handle reponse

                self._fetched.add(current_url)

            finally:
                self._q.task_done()

        @gen.coroutine
        def worker():
            while True:
                yield fetch_url()

        # Start workers, then wait for the work queue to be empty.
        for _ in range(self.concurrency):
            worker()

        yield self._q.join(timeout=timedelta(seconds=300000))

        try:
            assert self._fetching == self._fetched
        except AssertionError:    # some http error not handle
            self.logger.debug(self._fetching-self._fetched)
            self.logger.debug(self._fetched-self._fetching)

    def run(self):
        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self._run)


class MySpider(AsyncSpider):

    def fetch(self, url, **kwargs):
        """重写父类fetch方法可以添加cookies，headers，timeout等信息"""
        cookies_str = "PHPSESSID=j1tt66a829idnms56ppb70jri4; pspt=%7B%22id%22%3A%2233153%22%2C%22pswd%22%3A%228835d2c1351d221b4ab016fbf9e8253f%22%2C%22_code%22%3A%22f779dcd011f4e2581c716d1e1b945861%22%7D; key=%E9%87%8D%E5%BA%86%E5%95%84%E6%9C%A8%E9%B8%9F%E7%BD%91%E7%BB%9C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8; think_language=zh-cn; SERVERID=a66d7d08fa1c8b2e37dbdc6ffff82d9e|1444973193|1444967835; CNZZDATA1254842228=1433864393-1442810831-%7C1444972138"
        headers = {
            'User-Agent': 'mozilla/5.0 (compatible; baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            'cookie': cookies_str
        }
        return super(MySpider, self).fetch(
            url, headers=headers,
            #proxy_host="127.0.0.1", proxy_port=8787,    # for proxy
        )

    def handle_html(self, url, html):
        print(url)
        print(html)
        #print(BeautifulSoup(html, 'lxml').find('title'))


def main():
    st = time.time()
    urls = []
    n = 1000
    for page in range(1, n):
        # urls.append('http://www.jb51.net/article/%s.htm' % page)
        url = 'https://www.sov5.com/suggest?wd=i&p=3&cb=BaiduSuggestion.callbacks.give1481039919331&t=1481040157120&page=%d'%page
        urls.append(url)
    s = MySpider(urls, 20)
    s.run()
    print(time.time()-st)
    print(60.0/(time.time()-st)*1000, 'per minute')
    print(60.0/(time.time()-st)*1000/60.0, 'per second')


if __name__ == '__main__':
    main()
