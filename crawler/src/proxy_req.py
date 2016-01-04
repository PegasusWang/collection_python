#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

# install lantern first
proxies = {
    "http": "http://127.0.0.1:8787",
    "https": "http://127.0.0.1:8787",
}

url = 'http://google.com'
r = requests.get(url, proxies=proxies)
print(r.text)
