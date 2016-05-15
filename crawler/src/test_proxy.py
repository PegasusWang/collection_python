#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
try:
    from proxylib import get_addr
    addr, ip = get_addr()
except Exception as e:
    addr, ip = ('45.33.114.25', 18436L)
print(addr, ip)


import requesocks as requests
session = requests.session()
socks_proxies= {'http': 'socks5://%s:%d'%(addr, int(ip)),
                'https': 'socks5://%s:%d'%(addr, int(ip))}
print(socks_proxies)
session.proxies = socks_proxies
resp = session.get('https://api.ipify.org?format=json')
print(resp.status_code)
print(resp.headers['content-type'])
print(resp.text)


"""
print('http')
http_proxies = {
    "http": "http://%s:%d" % (addr, int(ip)),
    "https":"http://%s:%d" % (addr, int(ip)),
}
print(http_proxies)

r = requests.get('https://api.ipify.org?format=json')
print("Init IP is: " + r.text.replace("\n", ""))

r = requests.get('http://api.ipify.org?format=json', proxies=http_proxies)
print("Init IP is: " + r.text.replace("\n", ""))
"""

"""
import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr, ip)
socket.socket = socks.socksocket
import urllib2
print urllib2.urlopen('http://baidu.com').read()
"""
