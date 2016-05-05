#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
chrome有个功能，对于请求可以直接右键copy as curl，然后在命令行里边用curl
模拟发送请求。现在需要把此curl字符串处理成requests库可以传入的参数格式，
用python脚本更好的进行模拟。可以用来发广告机器人
暂时测试网址：tech2ipo.com; liwushuo.com
http://stackoverflow.com/questions/23118249/whats-the-difference-between-request-payload-vs-form-data-as-seen-in-chrome
"""

import json
import re
import requests
try:
    from urllib import urlencode  # py2
except ImportError:
    from urllib.parse import urlencode  # py3


tech2ipo_str = """
curl 'https://cn.avoscloud.com/1.1/functions/PostTxt.new' -H 'origin: http://tech2ipo.com' -H 'accept-encoding: gzip, deflate' -H 'accept-language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'content-type: text/plain' -H 'accept: */*' -H 'referer: http://tech2ipo.com/10026690' --data-binary $'{"post_id":"5685139100b01b9f2be8e5ab","txt":"\u5bb6\u5ead\u6559\u80b2","_ApplicationId":"qatav4vek3wbpsidrv867us5ootbnkxt9l1pw7ppz16rrfzc","_ApplicationKey":"zio0z5lb0mramk7z6akn7dakmw2bb015s3r8d4e9izqnmveq","_ApplicationProduction":0,"_ClientVersion":"js0.5.4","_InstallationId":"f83f19ae-e110-1bf0-df0b-e069607a0e29","_SessionToken":"e7wsvkygs3mrewz8ssumql9vj"}' --compressed
"""

liwushuo_str = """
curl 'http://www.liwushuo.com/api/posts/1022318/comments' -H 'Cookie: next_url=http://www.liwushuo.com/; _gat=1; session=6fa80dcf-af05-49ea-a935-18d455eb29f6; Hm_lvt_8a996f7888dea2ea6d5611cd24318338=1452052061,1452136889,1452138175,1452138280; Hm_lpvt_8a996f7888dea2ea6d5611cd24318338=1452158617; _ga=GA1.3.477073430.1452046529' -H 'X-NewRelic-ID: UQQAUlFTGwQBUFBRAQQ=' -H 'Origin: http://www.liwushuo.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://www.liwushuo.com/posts/1022318' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'content=beautiful' --compressed
"""


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


def test_liwushuo():
    url, headers, data = parse_curl_str(liwushuo_str)
    # data = urlencode([tuple('content=requests测试'.split('='))])
    data_str = 'content=测试12:05'
    data = urlencode(encode_to_dict(data_str))
    r = requests.post(url, data=data, headers=headers)
    print(r.content)

#test_liwushuo()


def test_tech2ipo():
    url, headers, data = parse_curl_str(tech2ipo_str)
    r = requests.post(url, json=json.loads(data), headers=headers)  # loads
    print(r.content)

#test_tech2ipo()


if __name__ == '__main__':
    import sys
    from pprint import pprint
    try:
        curl_str = sys.argv[1]
        url, headers, data = parse_curl_str(curl_str)
        print(url)
        pprint(headers)
        print(data)
    except IndexError:
        pass
