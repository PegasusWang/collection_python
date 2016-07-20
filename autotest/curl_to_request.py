#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import json
from pprint import pprint
import requests

# http://python-future.org/compatible_idioms.html
try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError


def parse_curl_str(s):
    """Convert chrome curl string to url, headers dict and data string
    解析copy as curl得到的字符串，返回url， header字典，post的数据(str)
    :param s: 右键chrome请求点击copy as curl得到的字符串。
    """
    pat = re.compile("'(.*?)'")
    str_list = [i.strip() for i in re.split(pat, s)]   # 拆分curl请求字符串

    url = ''
    headers_dict = {}
    data_str = ''

    for i in range(0, len(str_list)-1, 2):
        arg = str_list[i]
        string = str_list[i+1]

        if arg.startswith('curl'):
            url = string

        elif arg.startswith('-H'):
            header_key = string.split(':', 1)[0].strip()
            header_val = string.split(':', 1)[1].strip()
            headers_dict[header_key] = header_val

        elif arg.startswith('--data'):
            data_str = string

    return url, headers_dict, data_str



if __name__ == '__main__':
    s = """'curl http://pre3.papayamobile.com:1267/shoptimize/product/get_category_ids' -H 'Cookie: language=zh_CN; _gat=1; ppysid="PMs5bkeZejk5DZ9YuE+XRySRFW58DvWlgNYfI2YP+SQ="; save=true; email=fan_ll%40qq.com; password=6be037423107205d176a1d0d174402fac6b1dcc3d1b99b894fdbdf1d52ea9935; login_type=pmd; Hm_lvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463108257; Hm_lpvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463587952; _ga=GA1.2.2053141674.1463108258' -H 'Origin: http://pre3.papayamobile.com:1267' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://pre3.papayamobile.com:1267/shoptimize/campaign?type=website' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'product_type=0&account_id=2' --compressed"""
    pprint(parse_curl_str(s))
