#!/usr/bin/env python
# -*- coding:utf-8 -*-

# requests proxy demo
import requests

# install lantern first, 这是使用lantern的代理地址
proxies = {
    "http": "http://127.0.0.1:8787",
    "https": "http://127.0.0.1:8787",
}

url = 'http://httpbin.org/ip'
r = requests.get(url, proxies=proxies)
print(r.text)


# requests from version 2.10.0 support socks proxy
# pip install -U requests[socks]
proxies = {'http': "socks5://myproxy:9191"}
requests.get('http://example.org', proxies=proxies)

# tornado proxy demo
# sudo apt-get install libcurl-dev librtmp-dev
# pip install tornado pycurl

'''
from tornado import httpclient, ioloop

config = {
    'proxy_host': 'YOUR_PROXY_HOSTNAME_OR_IP_ADDRESS',
    'proxy_port': 3128
}

httpclient.AsyncHTTPClient.configure(
    "tornado.curl_httpclient.CurlAsyncHTTPClient")


def handle_request(response):
    if response.error:
        print "Error:", response.error
    else:
        print response.body
    ioloop.IOLoop.instance().stop()

http_client = httpclient.AsyncHTTPClient()
http_client.fetch("http://twitter.com/",
    handle_request, **config)
ioloop.IOLoop.instance().start()
'''
