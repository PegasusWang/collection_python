#!/usr/bin/env python
# -*- coding:utf-8 -*-

# requests proxy demo
import requests

# install lantern first
proxies = {
    "http": "http://127.0.0.1:8787",
    "https": "http://127.0.0.1:8787",
}

url = 'http://google.com'
r = requests.get(url, proxies=proxies)
print(r.text)






# tornado proxy demo
# sudo apt-get install libcurl-dev librtmp-dev
# pip install tornado pycurl

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
