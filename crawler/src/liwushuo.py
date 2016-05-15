#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import time
from datetime import timedelta
from tornado import httpclient, gen, ioloop, queues
import traceback
from extract import extract
from bs4 import BeautifulSoup
import json
import re
import requests
try:
    from urllib import urlencode  # py2
except ImportError:
    from urllib.parse import urlencode  # py3


def get_logger(name):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    return logger


class AsyncSpider(object):
    """A simple class of asynchronous spider."""
    def __init__(self, urls, concurrency=10, results=None, **kwargs):
        self.concurrency = concurrency
        self._q = queues.Queue()
        self._fetching = set()
        self._fetched = set()
        if results is None:
            self.results = []
        for url in urls:
            self._q.put(url)
        self.logger = get_logger(self.__class__.__name__)
        httpclient.AsyncHTTPClient.configure(
            "tornado.curl_httpclient.CurlAsyncHTTPClient"
        )

    def fetch(self, url, **kwargs):
        fetch = getattr(httpclient.AsyncHTTPClient(), 'fetch')
        return fetch(url, raise_error=False, **kwargs)

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
        # yield gen.sleep(10)    # sleep when need
        try:
            response = yield self.fetch(url)
            self.logger.debug('######fetched %s' % url)
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
        except AssertionError:
            print(self._fetching-self._fetched)
            print(self._fetched-self._fetching)

    def run(self):
        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self._run)


tech2ipo_str = """
curl 'https://cn.avoscloud.com/1.1/functions/PostTxt.new' -H 'origin: http://tech2ipo.com' -H 'accept-encoding: gzip, deflate' -H 'accept-language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'content-type: text/plain' -H 'accept: */*' -H 'referer: http://tech2ipo.com/10026690' --data-binary $'{"post_id":"5685139100b01b9f2be8e5ab","txt":"\u5bb6\u5ead\u6559\u80b2","_ApplicationId":"qatav4vek3wbpsidrv867us5ootbnkxt9l1pw7ppz16rrfzc","_ApplicationKey":"zio0z5lb0mramk7z6akn7dakmw2bb015s3r8d4e9izqnmveq","_ApplicationProduction":0,"_ClientVersion":"js0.5.4","_InstallationId":"f83f19ae-e110-1bf0-df0b-e069607a0e29","_SessionToken":"e7wsvkygs3mrewz8ssumql9vj"}' --compressed
"""

#liwushuo_str = """curl 'http://www.liwushuo.com/api/posts/1022318/comments' -H 'Cookie: next_url=http://www.liwushuo.com/; _gat=1; session=6fa80dcf-af05-49ea-a935-18d455eb29f6; Hm_lvt_8a996f7888dea2ea6d5611cd24318338=1452052061,1452136889,1452138175,1452138280; Hm_lpvt_8a996f7888dea2ea6d5611cd24318338=1452158617; _ga=GA1.3.477073430.1452046529' -H 'X-NewRelic-ID: UQQAUlFTGwQBUFBRAQQ=' -H 'Origin: http://www.liwushuo.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://www.liwushuo.com/posts/1022318' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'content=beautiful' --compressed"""
#liwushuo_str = """curl 'http://www.liwushuo.com/api/posts/1030176/comments' -H 'Cookie: session=83288823-1a8f-475b-a828-f13dc6d7a1ea; _gat=1; post_1030176=true; Hm_lvt_8a996f7888dea2ea6d5611cd24318338=1452524414; Hm_lpvt_8a996f7888dea2ea6d5611cd24318338=1452524503; _ga=GA1.3.753266897.1452524415' -H 'X-NewRelic-ID: UQQAUlFTGwQBUFBRAQQ=' -H 'Origin: http://www.liwushuo.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://www.liwushuo.com/posts/1030176' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'content=%E7%9A%84' --compressed"""
liwushuo_str="""curl 'http://www.liwushuo.com/api/posts/1029875/comments' -H 'Cookie: _gat=1; next_url=http://www.liwushuo.com/; post_1029875=true; session=0a21bd76-6e3c-42c5-9992-779edd102e45; Hm_lvt_8a996f7888dea2ea6d5611cd24318338=1452527237; Hm_lpvt_8a996f7888dea2ea6d5611cd24318338=1452527345; _ga=GA1.3.1343556402.1452527238' -H 'X-NewRelic-ID: UQQAUlFTGwQBUFBRAQQ=' -H 'Origin: http://www.liwushuo.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://www.liwushuo.com/posts/1029875' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'content=Murphy's Law' --compressed"""


def encode_to_dict(encoded_str):
    """ 将encode后的数据拆成dict
    >>> encode_to_dict('name=foo')
    {'name': foo'}
    >>> encode_to_dict('name=foo&val=bar')
    {'name': 'foo', 'val': 'var'}
    """

    pair_list = encoded_str.split('&')
    d = {}
    for pair in pair_list:
        if pair:
            key = pair.split('=')[0]
            val = pair.split('=')[1]
            d[key] = val
    return d


def parse_curl_str(s):
    pat = re.compile("'(.*?)'")
    str_list = [i.strip() for i in re.split(pat, s)]   # 拆分curl请求字符串

    url = ''
    headers = {}
    data = ''

    for i in range(0, len(str_list)-1, 2):
        arg = str_list[i]
        string = str_list[i+1]

        if arg.startswith('curl'):
            url = string

        elif arg.startswith('-H'):
            header_key = string.split(':', 1)[0].strip()
            header_val = string.split(':', 1)[1].strip()
            headers[header_key] = header_val

        elif arg.startswith('--data'):
            data = string

    return url, headers, data


def test_liwushuo():
    url, headers, data = parse_curl_str(liwushuo_str)
    # data = urlencode([tuple('content=requests测试'.split('='))])
    data_str = 'content=轰炸测试'
    data = urlencode(encode_to_dict(data_str))
    r = requests.post(url, data=data, headers=headers)
    print(r.content)

#test_liwushuo()


class LiwushuoPost(AsyncSpider):

    def fetch(self, url, **kwargs):
        """重写父类fetch方法可以添加cookies，headers，timeout等信息"""
        url, headers, data = parse_curl_str(url)
        #data_str = 'content=Murphy Law' + str(int(time.time()))
        data_str = """content=http://www.meilishuo.com/"""
        data = urlencode(encode_to_dict(data_str))    # encode chinese
        return super(LiwushuoPost, self).fetch(
            url, method="POST", headers=headers, body=data,
            proxy_host="127.0.0.1", proxy_port=8787,
        )

    def handle_html(self, url, html):
        #title = extract('<title>', '</title>', html.decode('gb18030'))
        #print(url, title)
        #print(BeautifulSoup(html).find('title'))
        print(url, html)


def main():
    proxies = {
        "http": "http://127.0.0.1:8787",
        "https": "http://127.0.0.1:8787",
    }
    st = time.time()
    urls = []
    n = 2
    liwushuo_str="""curl 'http://www.liwushuo.com/api/posts/%s/comments' -H 'Cookie: _gat=1; next_url=http://www.liwushuo.com/; post_1029875=true; session=0a21bd76-6e3c-42c5-9992-779edd102e45; Hm_lvt_8a996f7888dea2ea6d5611cd24318338=1452527237; Hm_lpvt_8a996f7888dea2ea6d5611cd24318338=1452527345; _ga=GA1.3.1343556402.1452527238' -H 'X-NewRelic-ID: UQQAUlFTGwQBUFBRAQQ=' -H 'Origin: http://www.liwushuo.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://www.liwushuo.com/posts/1029875' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'content=Murphy's Law' --compressed"""
    item_url = "http://www.liwushuo.com/api/channels/1/items?limit=12&offset=12"
    offset = 0
    limit = 20
    while offset < 100:
        content = requests.get("http://www.liwushuo.com/api/channels/1/items?limit=%d&offset=%d"%(limit, offset),
                               proxies=proxies).text
        offset += 20
        o = json.loads(content)
        try:
            for i in o.get('data').get('items'):
                post_id = i.get('id')
                urls.append(liwushuo_str%post_id)
        except Exception:
            traceback.print_exc()
            continue

    '''
    for page in range(1, n):
        #urls.append('http://www.jb51.net/article/%s.htm' % page)
        url, headers, data = parse_curl_str()
        urls.append(url+'?page=%d'%page)
    '''
    s = LiwushuoPost(urls, 10)
    s.run()
    print(time.time()-st)
    print(60.0/(time.time()-st)*1000, 'per minute')
    print(60.0/(time.time()-st)*1000/60.0, 'per second')


if __name__ == '__main__':
    main()
