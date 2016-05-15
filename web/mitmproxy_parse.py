#!/usr/bin/env python
# -*- coding:utf-8 -*-


import json
import re
import requests
try:
    from urllib import urlencode  # py2
except ImportError:
    from urllib.parse import urlencode  # py3

def headers_to_dict(s):
    arg_list = [line.strip() for line in s.split('\n')]
    d = {}
    for i in arg_list:
        if i:
            k = i.split(':')[0].strip()
            v = i.split(':')[1].strip()
            d[k] = v
    return d

HEADERS = """
Accept: text/xml, text/html, application/xhtml+xml, image/png, text/plain, */*;q=0.8
User-Agent: Mozilla/5.0 (Linux; U; Android 5.0.2; zh-cn; XT1079 Build/LXB22.99-7.1) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1 MicroMessenger/6.3.9.48_refecd3e.700 NetType/WIFI Language/zh_CN
Accept-Language: zh-CN
Accept-Charset: utf-8, iso-8859-1, utf-16, *;q=0.7
Accept-Encoding: gzip
Host: mp.weixin.qq.com
Cookie: pgv_pvi=9139880960
Q-UA2: QV=2&PL=ADR&PR=TBS&PB=GE&VE=B1&VN=1.5.0.1069&CO=X5&COVN=025489&RF=PRI&PP=com.tencent.mm&PPVC=26030930&RL=720*1184&MO= XT1079 &DE=PHONE&OS=5.0.2&API=21&CHID=0&LCID=9422
Q-GUID: a7804fba4599e8b117df5b6913b788cb
Q-Auth: 31045b957cf33acf31e40be2f3e71c5217597676a9729f1b
Content-Length: 0
"""


url = 'http://mp.weixin.qq.com/s?__biz=MzA3NTEzMTUwNA==&f=json&mid=206110593&idx=1&sn=bbebeb601bec2cd9bb576f31601774c5&scene=4#wechat_redirect'
url = 'http://mp.weixin.qq.com/mp/getappmsgext?__biz=MzA3NTEzMTUwNA==&f=json&mid=206110593&idx=1&sn=bbebeb601bec2cd9bb576f31601774c5&scene=4#wechat_redirect'
r = requests.get(url, headers=headers_to_dict(HEADERS), verify=0)
print(r.content)
