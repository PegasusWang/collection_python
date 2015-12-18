#!/usr/bin/env python
#coding:utf-8
import _env
from _gearman import gearman

index = gearman.client('search.index', True)

import hyperestraier
from z42.config import HYPERESTRAIER
import base64

class Transport(object):
    def __init__(self):
        self.url = None
        self.pxhost = None
        self.pxport = 0
        self.timeout = 0
        self.auth = None

    def extract(self, callback):
        return callback(None)

    def sendAndExtract(self, command, callback, errback, extractCallback,
                       headers={}, body=None, autoContentType=True):
        result = self.send(command, callback, errback,
                           headers, body, autoContentType)
        return extractCallback(result)

    def callback(self, result):
        li = []
        count = 0
        if result:
            _iter =  iter(result.split("\n"))
            for i in _iter:
                i = i.split("\t",1)
                if i[0] == "HIT":
                    count = int(i[1])
                    break
            for i in _iter:
                if i.startswith("@uri="):
                    li.append(int(i[5:]))
        return li, count


    def send(self, command, callback, errback,
             headers={}, body=None, autoContentType=True):


        return self._send(command, headers, body)
#        try:
#            status, result = self._send(command, headers, body)
#            return callback(result)
#        except urllib2.HTTPError, e:
#            status, result = e.code, str(e)
#        except Exception, e:
#            status, result =  -1, str(e)
#        return errback(result)


    def _send(self, command, headers={}, body=None, autoContentType=True):
        if not self.url:
            raise UrlNotSpecifiedException

        url = self.url + '/' + command
        headers = headers.copy()
        if 'Content-Type' not in headers and autoContentType:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        if self.auth:
            encodedAuth = base64.encodestring(self.auth).replace('\n', '')
            headers['Authorization'] = 'Basic ' + encodedAuth
        if body:
            headers['Content-Length'] = '%d' % len(body)

        self.headers = headers
        self.url = url
        self.body = body

        # TODO: set timeout
        #request = urllib2.Request(url)
        #if self.pxhost and self.pxport:
        #    request.set_proxy(self.pxhost, self.pxport)
        #request.add_data(body)
        #for k,v in headers.iteritems():
        #    request.add_header(k, v)
        #response = urllib2.urlopen(request)
        #result = response.read()
        #code = response.code

        #return code, result.decode("utf-8", "replace")

def search(db, txt, limit, offset):
    transport = Transport()
    node = hyperestraier.Node(transport)
    node.set_url(HYPERESTRAIER.URL+db)
    node.set_auth(HYPERESTRAIER.USER, HYPERESTRAIER.PASSWORD)
    node.set_snippet_width(0, 0, 0)
    cond = hyperestraier.Condition()
    if limit:
        cond.set_max(limit)
    #help(cond)
    cond.set_skip(offset)
    txt = txt.lower()
    txt = ' AND '.join(txt.split())
    cond.set_phrase(txt)
    node.search(cond, 0)
    return transport

if __name__ == '__main__':
    import random
    from random import randint
    # for i in xrange(1000,1200):
    #     index('test', i, '375956667 zspx', 1200 - i)
    # index('test', 1234, '中文 字符 文本 百度搜索 中文搜索')
    transport = search('ob0', '仝华帅', 100, 0)
    # index('ob0', 100001696, '嘀嘀打车')
    # transport = search('ob20000', '嘀嘀打车', 100, 0)
    import requests
    r = requests.post(transport.url, headers=transport.headers, data=transport.body)
    print transport.callback(r.content)


