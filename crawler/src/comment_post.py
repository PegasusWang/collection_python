#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""评论机器人，使用方法：评论的时候用浏览器捕捉post请求，然后右键copy as curl
把得到的字符串拷贝出来，代码会将curl命令解析成requests等库需要传入的字典"""


import time
from datetime import timedelta
from tornado import httpclient, gen, ioloop, queues
import traceback
from bs4 import BeautifulSoup
import json
import re
import requests
try:
    from urllib import urlencode  # py2
except ImportError:
    from urllib.parse import urlencode  # py3


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

        yield self._q.join(timeout=timedelta(seconds=60*60*24))
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
#liwushuo_str = """curl 'http://www.liwushuo.com/api/posts/1030667/comments' -H 'Cookie: _gat=1; next_url=http://www.liwushuo.com/; session=6fa80dcf-af05-49ea-a935-18d455eb29f6; post_1030667=true; _ga=GA1.3.477073430.1452046529; Hm_lvt_8a996f7888dea2ea6d5611cd24318338=1452052061,1452136889,1452138175,1452138280; Hm_lpvt_8a996f7888dea2ea6d5611cd24318338=1452329576' -H 'X-NewRelic-ID: UQQAUlFTGwQBUFBRAQQ=' -H 'Origin: http://www.liwushuo.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://www.liwushuo.com/posts/1030667' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'content=%E8%AF%84%E8%AE%BA' --compressed"""


#jb51_str = """curl 'http://changyan.sohu.com/api/2/comment/submit' -H 'Origin: http://www.jb51.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://www.jb51.net/article/47995.htm' -H 'Cookie: debug_uuid=C6E973CE11000001C936FF4316707E10; SSRU=http://changyan.sohu.com/api/oauth/refresh?connName=null&url=null&; SSTYPE=pc; SSAPPID=30000001; ppinf=2|1452480104|0|bG9naW5pZDowOnx1c2VyaWQ6NDQ6NkI5N0Y3NEM2RDYxMjdFQUY3RjRCRTIxNzU1MjhEMDNAcXEuc29odS5jb218c2VydmljZXVzZTozMDowMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDB8Y3J0OjA6fGVtdDoxOjB8YXBwaWQ6NDoxMDE5fHRydXN0OjE6MXxwYXJ0bmVyaWQ6MTowfHJlbGF0aW9uOjA6fHV1aWQ6MTY6OTQ4YjQ1YTVlMGRmNGJleHx1aWQ6MTY6OTQ4YjQ1YTVlMGRmNGJleHx1bmlxbmFtZToxNjp2aXNpdG9yNTIzNDkzMDQ2fHJlZnVzZXJpZDozMjo2Qjk3Rjc0QzZENjEyN0VBRjdGNEJFMjE3NTUyOEQwM3xyZWZuaWNrOjQ6cGx1c3w; pprdig=TkVGwkyQq5BTxALqYIrlssKWthK2gwV5GMRUBuEJZ4XAjhGx8ZEgcmld1Y4E_tFWzpVqJaVFECo377_EDraNHVu-VFhuORIM_3JQAKXzgWeT5EHqjBTxyCinqrghNXKRxBNzYefK9jxI1yFBw_bxKvmYHmdybPNUT4RTefIkLa0; passport=1|1452480104|0|dXNlcmlkOjQ0OjZCOTdGNzRDNkQ2MTI3RUFGN0Y0QkUyMTc1NTI4RDAzQHFxLnNvaHUuY29tfHNlcnZpY2V1c2U6MzA6MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwfA|a|iH2nPTOF1OuFG5PA3SK2jf7z7ITj4Iu2iuyNSYB50P4zntnbqwVK9jom7BAhHIBK1QLm4pA0wtRiJvwTdGYagWFjtiJu_8lDlTFzU9i4lkryBuCWoDLNLkKRhnHmci8uTuzcEOCMC8bRV8pjccJr1ao4VwwVUuXyUkhJRWMNQuQ; spinfo=cXF8NkI5N0Y3NEM2RDYxMjdFQUY3RjRCRTIxNzU1MjhEMDN8MzQ3MzM3NTA3; ppmdig=1452480104000000db6ed77df501c69afb0759ae7babb8e8; front-end-refresh=refresh; JSESSIONID=aaaWUiWqCeV7VgPZDaBiv; spsession=MzQ3MzM3NTA3fDE0NTMwODUwMTJ8MTQ1NTA3MjEwNHxxcTM0NzMzNzUwNw==-nhAOSy1Pztts2gwmTZ0jrPChtno=' -H 'Connection: keep-alive' --data 'client_id=cyrHH3dwi&topic_id=601579207&content=%E6%80%8E%E4%B9%88%E6%B2%A1%E4%BA%86&cmt_bold=false&cmt_color=false&topic_title=%25E5%2588%2586%25E4%25BA%25AB%25E4%25B8%258B%25E7%25BD%2591%25E7%25AB%2599%25E5%25BC%2580%25E5%258F%2591%25E4%25BA%25BA%25E5%2591%2598%25E5%25BA%2594%25E8%25AF%25A5%25E7%259F%25A5%25E9%2581%2593%25E7%259A%258461%25E4%25BB%25B6%25E4%25BA%258B_%25E5%2585%25B6%25E5%25AE%2583%25E7%25BB%25BC%25E5%2590%2588_%25E8%2584%259A%25E6%259C%25AC%25E4%25B9%258B%25E5%25AE%25B6&topic_url=http%253A%252F%252Fwww.jb51.net%252Farticle%252F47995.htm&dataType=&cmtNum=&floorNum=&attachment_urls=' --compressed"""
#jb51_str = """curl 'http://changyan.sohu.com/api/2/comment/submit' -H 'Origin: http://www.jb51.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://www.jb51.net/article/47995.htm' -H 'Cookie: vjuids=-ce5b1387f.14a1e3e9a95.0.3b0fe39a; debug_uuid=C68A4C5B627000019A59934C4CE014C8; IPLOC=CN1100; SUV=1501251007274375; _ga=GA1.2.2112116122.1450511498; vjlast=1417846627.1452149942.11; sohutag=8HsmeSc5NSwmcyc5NCwmYjc5NCwmYSc5NCwmZjc5NCwmZyc5NCwmbjc5MCwmaSc5NSwmdyc5NCwmaCc5NCwmYyc5NCwmZSc5NjwmbSc5NCwmdCc5NH0; SSRU=http://changyan.sohu.com/api/oauth/refresh?connName=null&url=null&; SSTYPE=pc; SSAPPID=30000001; spinfo=dmlzaXRvcnxzOTg5MTBkNTkzNmQwZmYwQHNvaHUuY29tfDM0NzMzNzU1NA==; ppinf=2|1452480376|0|bG9naW5pZDowOnx1c2VyaWQ6MjU6czk4OTEwZDU5MzZkMGZmMEBzb2h1LmNvbXxzZXJ2aWNldXNlOjMwOjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMHxjcnQ6MTA6MjAxNi0wMS0xMXxlbXQ6MTowfGFwcGlkOjQ6MTAxOXx0cnVzdDoxOjF8cGFydG5lcmlkOjE6MHxyZWxhdGlvbjowOnx1dWlkOjE2OjU4N2I0YjAyNTMxNzQ2N3N8dWlkOjE2OjU4N2I0YjAyNTMxNzQ2N3N8dW5pcW5hbWU6MTI6czk4OTEwZDU5MzZkfA; pprdig=b_nJ3jfi2uV0LmSFfIfL0icBCgXqrp1w1yriI3My1iKB5-CZ8fbaUCMLMaZBG5pycTH6QWVOMKwrQcdV02UnlFiOa7lkK9hJ6c7p_4aSm92YOyhRMz7cM8H6Qa39GWgkRTAW6iCdLSfuig1vD961uyA3p7Y82HmetwGzh0_1Bl0; passport=1|1452480376|0|dXNlcmlkOjI1OnM5ODkxMGQ1OTM2ZDBmZjBAc29odS5jb218c2VydmljZXVzZTozMDowMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDB8|a|IC0Kgz3nXj1gDW2jdiPP3f3sGMqzyr0dnO9Bd5XE8jgPdMzBKB0jfuvMkYX7U-s98e_0CZrCC0o_5K8Xj_yvhLk1qHeUetWJKzXCd2HkJWriuFFXJLtVm3sScR3YHvIqiGRONQAfIuwOs1ucysswAcYg9ig0ID-FIoNzXueSuPQ; ppmdig=1452480380000000df993d8caa951cd820dea4c22504dd8d; spsession=MzQ3MzM3NTU0fDE0NTUwNzIzNzZ8MTQ2ODAzMjM3NnxzOTg5MTBkNTkzNmQwZmY=-92hlr5aLAcOhDwRhuR8chies4k8=' -H 'Connection: keep-alive' --data 'client_id=cyrHH3dwi&topic_id=601579207&content=%E5%91%B5%E5%91%B5&cmt_bold=false&cmt_color=false&topic_title=%25E5%2588%2586%25E4%25BA%25AB%25E4%25B8%258B%25E7%25BD%2591%25E7%25AB%2599%25E5%25BC%2580%25E5%258F%2591%25E4%25BA%25BA%25E5%2591%2598%25E5%25BA%2594%25E8%25AF%25A5%25E7%259F%25A5%25E9%2581%2593%25E7%259A%258461%25E4%25BB%25B6%25E4%25BA%258B_%25E5%2585%25B6%25E5%25AE%2583%25E7%25BB%25BC%25E5%2590%2588_%25E8%2584%259A%25E6%259C%25AC%25E4%25B9%258B%25E5%25AE%25B6&topic_url=http%253A%252F%252Fwww.jb51.net%252Farticle%252F47995.htm&dataType=&cmtNum=&floorNum=&attachment_urls=' --compressed"""
#jb51_str = """curl 'http://changyan.sohu.com/api/2/comment/submit' -H 'Origin: http://www.jb51.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://www.jb51.net/article/47995.htm' -H 'Cookie: vjuids=-ce5b1387f.14a1e3e9a95.0.3b0fe39a; debug_uuid=C68A4C5B627000019A59934C4CE014C8; IPLOC=CN1100; SUV=1501251007274375; _ga=GA1.2.2112116122.1450511498; vjlast=1417846627.1452149942.11; sohutag=8HsmeSc5NSwmcyc5NCwmYjc5NCwmYSc5NCwmZjc5NCwmZyc5NCwmbjc5MCwmaSc5NSwmdyc5NCwmaCc5NCwmYyc5NCwmZSc5NjwmbSc5NCwmdCc5NH0; SSRU=http://changyan.sohu.com/api/oauth/refresh?connName=null&url=null&; SSTYPE=pc; SSAPPID=30000001; spinfo=dmlzaXRvcnxzOTg5MTBkNTkzNmQwZmYwQHNvaHUuY29tfDM0NzMzNzU1NA==; ppinf=2|1452480376|0|bG9naW5pZDowOnx1c2VyaWQ6MjU6czk4OTEwZDU5MzZkMGZmMEBzb2h1LmNvbXxzZXJ2aWNldXNlOjMwOjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMHxjcnQ6MTA6MjAxNi0wMS0xMXxlbXQ6MTowfGFwcGlkOjQ6MTAxOXx0cnVzdDoxOjF8cGFydG5lcmlkOjE6MHxyZWxhdGlvbjowOnx1dWlkOjE2OjU4N2I0YjAyNTMxNzQ2N3N8dWlkOjE2OjU4N2I0YjAyNTMxNzQ2N3N8dW5pcW5hbWU6MTI6czk4OTEwZDU5MzZkfA; pprdig=b_nJ3jfi2uV0LmSFfIfL0icBCgXqrp1w1yriI3My1iKB5-CZ8fbaUCMLMaZBG5pycTH6QWVOMKwrQcdV02UnlFiOa7lkK9hJ6c7p_4aSm92YOyhRMz7cM8H6Qa39GWgkRTAW6iCdLSfuig1vD961uyA3p7Y82HmetwGzh0_1Bl0; passport=1|1452480376|0|dXNlcmlkOjI1OnM5ODkxMGQ1OTM2ZDBmZjBAc29odS5jb218c2VydmljZXVzZTozMDowMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDB8|a|IC0Kgz3nXj1gDW2jdiPP3f3sGMqzyr0dnO9Bd5XE8jgPdMzBKB0jfuvMkYX7U-s98e_0CZrCC0o_5K8Xj_yvhLk1qHeUetWJKzXCd2HkJWriuFFXJLtVm3sScR3YHvIqiGRONQAfIuwOs1ucysswAcYg9ig0ID-FIoNzXueSuPQ; ppmdig=1452480380000000df993d8caa951cd820dea4c22504dd8d; spsession=MzQ3MzM3NTU0fDE0NTUwNzIzNzZ8MTQ2ODAzMjM3NnxzOTg5MTBkNTkzNmQwZmY=-92hlr5aLAcOhDwRhuR8chies4k8=' -H 'Connection: keep-alive' --data 'client_id=cyrHH3dwi&topic_id=601579207&content=jiba51&cmt_bold=false&cmt_color=false&topic_title=%25E5%2588%2586%25E4%25BA%25AB%25E4%25B8%258B%25E7%25BD%2591%25E7%25AB%2599%25E5%25BC%2580%25E5%258F%2591%25E4%25BA%25BA%25E5%2591%2598%25E5%25BA%2594%25E8%25AF%25A5%25E7%259F%25A5%25E9%2581%2593%25E7%259A%258461%25E4%25BB%25B6%25E4%25BA%258B_%25E5%2585%25B6%25E5%25AE%2583%25E7%25BB%25BC%25E5%2590%2588_%25E8%2584%259A%25E6%259C%25AC%25E4%25B9%258B%25E5%25AE%25B6&topic_url=http%253A%252F%252Fwww.jb51.net%252Farticle%252F47995.htm&dataType=&cmtNum=&floorNum=&attachment_urls=' --compressed"""
jb51_str = """curl 'http://changyan.sohu.com/api/2/comment/submit' -H 'Origin: http://www.jb51.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://www.jb51.net/article/47995.htm' -H 'Cookie: debug_uuid=C6E98C936E60000140C11396194212A9; vid=62788f15-8331-447d-91f4-2b24465f1fb5; SSRU=http://changyan.sohu.com/api/oauth/refresh?connName=null&url=null&; SSTYPE=pc; SSAPPID=30000001; ppinf=2|1452506111|0|bG9naW5pZDowOnx1c2VyaWQ6NDQ6NkI5N0Y3NEM2RDYxMjdFQUY3RjRCRTIxNzU1MjhEMDNAcXEuc29odS5jb218c2VydmljZXVzZTozMDowMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDB8Y3J0OjA6fGVtdDoxOjB8YXBwaWQ6NDoxMDE5fHRydXN0OjE6MXxwYXJ0bmVyaWQ6MTowfHJlbGF0aW9uOjA6fHV1aWQ6MTY6OTQ4YjQ1YTVlMGRmNGJleHx1aWQ6MTY6OTQ4YjQ1YTVlMGRmNGJleHx1bmlxbmFtZToxNjp2aXNpdG9yNTIzNDkzMDQ2fHJlZnVzZXJpZDozMjo2Qjk3Rjc0QzZENjEyN0VBRjdGNEJFMjE3NTUyOEQwM3xyZWZuaWNrOjQ6cGx1c3w; pprdig=WJDO-h7zfaIQXjucnE_7eu57seETWBkkM0lRRyZBQTFGnQS9NSGcoGJiD3oUzM10xk0edVrJkGon3KZOvU63ooCJm5pZO__5Rs7djWZTYSLDMiH0zmhgXx6h22NSKv8uqIXc3qQmqcR8urU6Nmbby9-gsZ0G1b_6o5_ymrddVuM; passport=1|1452506111|0|dXNlcmlkOjQ0OjZCOTdGNzRDNkQ2MTI3RUFGN0Y0QkUyMTc1NTI4RDAzQHFxLnNvaHUuY29tfHNlcnZpY2V1c2U6MzA6MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwfA|a|eBe4ZaL1ZgnIAnGxLeO_LnoCth-7HCUEJp3OK4OwpWlWGcZLMQhp9vFswHCxgxlxBXZCkblknQZ-lWS2MJ2qLnW9qJKGuioYphI0FEeAST8UBS6RkMGwu2pGrhONZcrynpms3ECGA-VsiaNYKoSeOgDo6UFI4qS9Qff9v221S_c; spinfo=cXF8NkI5N0Y3NEM2RDYxMjdFQUY3RjRCRTIxNzU1MjhEMDN8MzQ3MzM3NTA3; spsession=MzQ3MzM3NTA3fDE0NTMxMTA5MTF8MTQ1NTA5ODExMXxxcTM0NzMzNzUwNw==-qXlAQUm0JFwiozWm256/uDeWGs0=; ppmdig=145250608600000088749941cd22adeea9d5201d8e33b58a; front-end-refresh=refresh; JSESSIONID=aaalUeNr87MihgnqWaBiv' -H 'Connection: keep-alive' --data 'client_id=cyrHH3dwi&topic_id=601579207&content=douniwan&cmt_bold=false&cmt_color=false&topic_title=%25E5%2588%2586%25E4%25BA%25AB%25E4%25B8%258B%25E7%25BD%2591%25E7%25AB%2599%25E5%25BC%2580%25E5%258F%2591%25E4%25BA%25BA%25E5%2591%2598%25E5%25BA%2594%25E8%25AF%25A5%25E7%259F%25A5%25E9%2581%2593%25E7%259A%258461%25E4%25BB%25B6%25E4%25BA%258B_%25E5%2585%25B6%25E5%25AE%2583%25E7%25BB%25BC%25E5%2590%2588_%25E8%2584%259A%25E6%259C%25AC%25E4%25B9%258B%25E5%25AE%25B6&topic_url=http%253A%252F%252Fwww.jb51.net%252Farticle%252F47995.htm&dataType=&cmtNum=&floorNum=&attachment_urls=' --compressed"""


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

class CommentPoster(AsyncSpider):

    def fetch(self, url, **kwargs):
        url, headers, data = parse_curl_str(jb51_str)
        return super(CommentPoster, self).fetch(
            url, method="POST", headers=headers, body=data
        )

    def handle_html(self, url, html):
        print(url, html)


def main():
    st = time.time()
    urls = []
    n = 100000
    for page in range(1, n):
        url, headers, data = parse_curl_str(jb51_str)
        urls.append(url+'?page=%d'%page)
    s = CommentPoster(urls, 20)
    s.run()
    print(time.time()-st)
    print(60.0/(time.time()-st)*1000, 'per minute')
    print(60.0/(time.time()-st)*1000/60.0, 'per second')


if __name__ == '__main__':
    main()
