#!/usr/bin/env python
# -*- coding:utf-8 -*-


import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient

def handle_request(response):
    '''callback needed when a response arrive'''
    if response.error:
        print "Error:", response.error
    else:
        print 'called'
        print response.body

http_client = AsyncHTTPClient()
for i in range(10):
    http_client.fetch("http://www.baidu.com", handle_request)
tornado.ioloop.IOLoop.instance().start()
