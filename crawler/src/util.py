#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
chrome有个功能，对于请求可以直接右键copy as curl，然后在命令行里边用curl
模拟发送请求。现在需要把此curl字符串处理成requests库可以传入的参数格式，
http://stackoverflow.com/questions/23118249/whats-the-difference-between-request-payload-vs-form-data-as-seen-in-chrome
"""

import re
from functools import wraps
import traceback
import requests


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
    """convert chrome curl string to url, headers_dict and data"""
    pat = re.compile("'(.*?)'")
    str_list = [i.strip() for i in re.split(pat, s)]   # 拆分curl请求字符串

    url = ''
    headers_dict = {}
    data = ''

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
            data = string

    return url, headers_dict, data


def retry(retries=3):
    """一个失败请求重试，或者使用下边这个功能强大的retrying
    pip install retrying
    https://github.com/rholder/retrying

    :param retries: number int of retry times.
    """
    def _retry(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            index = 0
            while index < retries:
                index += 1
                try:
                    response = func(*args, **kwargs)
                    if response.status_code == 404:
                        print(404)
                        break
                    elif response.status_code != 200:
                        print(response.status_code)
                        continue
                    else:
                        break
                except Exception as e:
                    traceback.print_exc()
                    response = None
            return response
        return _wrapper
    return _retry


_get = requests.get


@retry(5)
def get(*args, **kwds):
    if 'timeout' not in kwds:
        kwds['timeout'] = 10
    if 'headers' not in kwds:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        }
        kwds['headers'] = headers

    return _get(*args, **kwds)

requests.get = get
