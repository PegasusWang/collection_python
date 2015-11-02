#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

url = 'http://www.qichacha.com/firm_CN_58f30dedb356b5f911cfa5d5b60ba734'
cookies_str = 'PHPSESSID=j1tt66a829idnms56ppb70jri4; pspt=%7B%22id%22%3A%2233153%22%2C%22pswd%22%3A%228835d2c1351d221b4ab016fbf9e8253f%22%2C%22_code%22%3A%22f779dcd011f4e2581c716d1e1b945861%22%7D; key=%E8%85%BE%E8%AE%AF%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8; think_language=zh-cn; CNZZDATA1254842228=1433864393-1442810831-%7C1446426275; SERVERID=a66d7d08fa1c8b2e37dbdc6ffff82d9e|1446429273|1446429164'


def cookies_to_dict(s):
    arg_list = [line.strip() for line in s.split(';')]
    d = {}
    for i in arg_list:
        if i:
            k = i.split('=')[0].strip()
            v = i.split('=')[1].strip()
            d[k] = v
    return d
headers = {
    'cookie': cookies_str
}
r = requests.get(url, headers=headers).content
print r

"""
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
#for i in range(10):
http_client.fetch("http://www.baidu.com", handle_request)
tornado.ioloop.IOLoop.instance().start()
"""
