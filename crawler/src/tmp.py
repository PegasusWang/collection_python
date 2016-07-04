#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
chrome有个功能，对于请求可以直接右键copy as curl，然后在命令行里边用curl
模拟发送请求。现在需要把此curl字符串处理成requests库可以传入的参数格式，
http://stackoverflow.com/questions/23118249/whats-the-difference-between-request-payload-vs-form-data-as-seen-in-chrome
"""

import json
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


def retry_get_html(*args, **kwargs):
    try:
        return get(*args, **kwargs).content
    except AttributeError:
        return ''


def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
            return getattr(self, attr_name)
    return _lazy_property


def my_ip():
    # url = 'https://api.ipify.org?format=json'
    url = 'http://httpbin.org/ip'
    return requests.get(url).text


def form_data_to_dict(s):
    """form_data_to_dict

    :param s:
    """
    arg_list = [line.strip() for line in s.split('\n')]
    d = {}
    for i in arg_list:
        if i:
            k = i.split(':', 1)[0].strip()
            v = ''.join(i.split(':', 1)[1:]).strip()
            d[k] = v
    return d


def test():
    from urllib import urlencode
    S = """curl 'https://graph.facebook.com/v2.5/act_858751837556226/customaudiences?access_token=EAAI4BG12pyIBABlBq3OOBjvOgpSH2euXyk37LpslZBXKUXXfwaLJ3EnJuxwyrZCFmWt1gZCplMjBFvo50wX9uHWIKjVkM5OTFmyfr6vA1QNGpRjkTjZAxY0jPwpAPXIQ9i6e4iXc2EtbL7Tg7qATJPGAVUxrOOTq5KYCUSw2MwZDZD' -H 'origin: https://business.facebook.com' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'user-agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36' -H 'content-type: application/x-www-form-urlencoded' -H 'accept: */*' -H 'referer: https://business.facebook.com/' -H 'authority: graph.facebook.com' --data '__business_id=712764242174174&_reqName=path%3A%2Fact_858751837556226%2Fcustomaudiences&_reqSrc=adsDaoGraphDataMutator&accountId=858751837556226&creation_params=%7B%22combination_type%22%3A%22website%22%2C%22traffic_type%22%3A4%7D&description=&endpoint=%2Fact_858751837556226%2Fcustomaudiences&exclusions=%5B%7B%22type%22%3A%22website%22%2C%22retention_days%22%3A30%2C%22rule%22%3A%22%7B%5C%22and%5C%22%3A%5B%7B%5C%22or%5C%22%3A%5B%7B%5C%22url%5C%22%3A%7B%5C%22i_contains%5C%22%3A%5C%22%5C%22%7D%7D%5D%7D%5D%7D%22%2C%22rule_aggregation%22%3Anull%7D%5D&inclusions=%5B%7B%22type%22%3A%22website%22%2C%22retention_days%22%3A180%2C%22rule%22%3A%22%7B%5C%22and%5C%22%3A%5B%7B%5C%22or%5C%22%3A%5B%7B%5C%22url%5C%22%3A%7B%5C%22i_contains%5C%22%3A%5C%22%5C%22%7D%7D%5D%7D%5D%7D%22%2C%22rule_aggregation%22%3Anull%7D%5D&locale=zh_CN&method=post&name=tt&pixel_id=1792170334346121&prefill=true&pretty=0&subtype=combination&suppress_http_code=1' --compressed"""
    url, headers, data = parse_curl_str(S)

    params = r"""
    __business_id:712764242174174
    _reqName:path:/act_858751837556226/customaudiences
    _reqSrc:adsDaoGraphDataMutator
    accountId:858751837556226
    creation_params:{"combination_type":"website","traffic_type":4}
    description:
    endpoint:/act_858751837556226/customaudiences
    exclusions:[{"type":"website","retention_days":30,"rule":"{\"and\":[{\"or\":[{\"url\":{\"i_contains\":\"\"}}]}]}","rule_aggregation":null}]
    inclusions:[{"type":"website","retention_days":180,"rule":"{\"and\":[{\"or\":[{\"url\":{\"i_contains\":\"\"}}]}]}","rule_aggregation":null}]
    locale:zh_CN
    method:post
    name:741747
    pixel_id:1792170334346121
    prefill:true
    pretty:0
    subtype:combination
    suppress_http_code:1
    """
    form_data_dict = form_data_to_dict(params)
    form_str = urlencode(form_data_dict)
    print(form_data_dict)
    print(form_str)
    print(data)
    r = requests.post(url, headers=headers, data=form_str)
    print(r.content)


test()
