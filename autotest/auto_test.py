# -*- coding: utf-8 -*-

import re
import json
from pprint import pprint
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
    """Convert chrome curl string to url, headers dict and data string
    此函数用来作为单元测试中提交按钮的操作
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


def request_curl_str(s):
    url, headers, data = parse_curl_str(s)
    r = requests.post(url, data=data, headers=headers)
    return r


def assert_request_success(curl_str):
    response = request_curl_str(curl_str)
    assert response.status_code == 200
    html = response.text
    o = json.loads(html)
    pprint(o)
    assert o['ret'] == 0    # return success


def get_file_curl_list(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


def assert_many_requests(curl_str_list):
    for curl_str in curl_str_list:
        assert_request_success(curl_str)


if __name__ == '__main__':
    import sys
    try:
        filepath = sys.argv[1]
    except IndexError:
        exit()
    curl_str_list = get_file_curl_list(filepath)
    assert_many_requests(curl_str_list)
