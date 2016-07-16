# -*- coding: utf-8 -*-

"""一个自动测试脚本，对于一系列执行流程发的请求，都可以用chrome的右键
copy as curl命令copy得到一个字符串。 这个请求字符串包含了所有的该请求需要的参数。
在一个文本文件里一行贴一个curl_str, 比如一个创建流程发送了create，
create_campaign等请求，在chrome里右键
copy as curl命令把这个两个请求一行粘贴一个。假设该文件命名为str.txt。
执行"python auto_test.py str.txt"
即可挨个发送请求，可以避免多次手动点击。如果cookie串或者端口换了，
可以在最后从chrome里得到新的cookie，在该脚本执行前替换por和cookie。下便是
一个创建产品系列的执行流程，对应接口如下，把下边字符串单独拷贝到一个
文本文件str.txt，一行一个。如果port和ppysid更换了（会过期），可以从chrome
直接拷贝新的，在本脚本最后赋值。每次执行即可测试下边六个接口。
curl 'http://pre3.papayamobile.com:1267/shoptimize/camp/create' -H 'Cookie: language=zh_CN; ppysid="PMs5bkeZejlLtw5JZIOIqXC0cn55JU4wN1Ze8uKzYsg="; save=true; email=fan_ll%40qq.com; password=6be037423107205d176a1d0d174402fac6b1dcc3d1b99b894fdbdf1d52ea9935; login_type=pmd; _gat=1; Hm_lvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463367057; Hm_lpvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463628472; _ga=GA1.2.527261763.1463367057' -H 'Origin: http://pre3.papayamobile.com:1267' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://pre3.papayamobile.com:1267/shoptimize/campaign?type=website' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'existing=1&step=0&objective=3&adaccount=2&offer_id=701&campaign_id=4563' --compressed
curl 'http://pre3.papayamobile.com:1267/shoptimize/camp/create_targeting' -H 'Cookie: language=zh_CN; ppysid="PMs5bkeZejlLtw5JZIOIqXC0cn55JU4wN1Ze8uKzYsg="; save=true; email=fan_ll%40qq.com; password=6be037423107205d176a1d0d174402fac6b1dcc3d1b99b894fdbdf1d52ea9935; login_type=pmd; _gat=1; Hm_lvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463367057; Hm_lpvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463628472; _ga=GA1.2.527261763.1463367057' -H 'Origin: http://pre3.papayamobile.com:1267' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://pre3.papayamobile.com:1267/shoptimize/campaign?type=website' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'campaign_id=4563&step=1&country=%5B1%5D&os=0&device=%5B%5D&odm=%5B%5D&age_low=18&placement=%5B%220%22%2C%223%22%2C%224%22%5D&age_high=65&gender=0&age_step=&interest=%5B%5D&connections=%5B%5D&friends_of_connections=%5B%5D&excluded_connections=%5B%5D&audience=%5B%5D&event_type=7' --compressed
curl 'http://pre3.papayamobile.com:1267/shoptimize/camp/create_creative' -H 'Cookie: language=zh_CN; ppysid="PMs5bkeZejlLtw5JZIOIqXC0cn55JU4wN1Ze8uKzYsg="; save=true; email=fan_ll%40qq.com; password=6be037423107205d176a1d0d174402fac6b1dcc3d1b99b894fdbdf1d52ea9935; login_type=pmd; _gat=1; Hm_lvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463367057; Hm_lpvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463628472; _ga=GA1.2.527261763.1463367057' -H 'Origin: http://pre3.papayamobile.com:1267' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://pre3.papayamobile.com:1267/shoptimize/campaign?type=website' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'img_ids=%5B1075%5D&text_update=%5B%7B%22id%22%3A212%2C%22text%22%3A%7B%22title%22%3A%22123%22%2C%22name%22%3A%22123%22%2C%22body%22%3A%22123%22%2C%22description%22%3A%22123%22%7D%7D%5D&text_new=%5B%22%22%5D&filter_ids=%5B%7B%22filter_type%22%3A%22id%22%2C%22filter_operator%22%3A%22is%22%2C%22filter_q%22%3A%5B125106%5D%7D%5D&campaign_id=4563&targeting_id=1210&page_id=599379080235405&page_name=599379080235405(Shy_test)&creative_id=575&type=0&ad_link=0&action=2&step=2' --compressed
curl 'http://pre3.papayamobile.com:1267/shoptimize/camp/choose_dimension' -H 'Cookie: language=zh_CN; ppysid="PMs5bkeZejlLtw5JZIOIqXC0cn55JU4wN1Ze8uKzYsg="; save=true; email=fan_ll%40qq.com; password=6be037423107205d176a1d0d174402fac6b1dcc3d1b99b894fdbdf1d52ea9935; login_type=pmd; _gat=1; Hm_lvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463367057; Hm_lpvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463628472; _ga=GA1.2.527261763.1463367057' -H 'Origin: http://pre3.papayamobile.com:1267' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://pre3.papayamobile.com:1267/shoptimize/campaign?type=website' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'dim_select=%5B6%2C3%2C0%2C5%5D&targeting_id=1210&creative_id=575&num=1' --compressed
curl 'http://pre3.papayamobile.com:1267/shoptimize/camp/save_budget_bid' -H 'Cookie: language=zh_CN; ppysid="PMs5bkeZejlLtw5JZIOIqXC0cn55JU4wN1Ze8uKzYsg="; save=true; email=fan_ll%40qq.com; password=6be037423107205d176a1d0d174402fac6b1dcc3d1b99b894fdbdf1d52ea9935; login_type=pmd; _gat=1; Hm_lvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463367057; Hm_lpvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463628472; _ga=GA1.2.527261763.1463367057' -H 'Origin: http://pre3.papayamobile.com:1267' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://pre3.papayamobile.com:1267/shoptimize/campaign?type=website' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'step=3&targeting_id=1210&budget=1&budget_type=0&max_bid=0.01&start_time=2016-05-18+19&end_time=&ad_cap_tz=UTC+-07%3A00' --compressed
curl 'http://pre3.papayamobile.com:1267/shoptimize/camp/generate_ads' -H 'Cookie: language=zh_CN; ppysid="PMs5bkeZejlLtw5JZIOIqXC0cn55JU4wN1Ze8uKzYsg="; save=true; email=fan_ll%40qq.com; password=6be037423107205d176a1d0d174402fac6b1dcc3d1b99b894fdbdf1d52ea9935; login_type=pmd; _gat=1; Hm_lvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463367057; Hm_lpvt_4f18dfc7029aaa9ff0b37ede9b128ef4=1463628472; _ga=GA1.2.527261763.1463367057' -H 'Origin: http://pre3.papayamobile.com:1267' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://pre3.papayamobile.com:1267/shoptimize/campaign?type=website' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'node=0&url_type=1&creative_id=575&page_no=1&page_count=20' --compressed
"""

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


def request_curl_str(s):
    url, headers, data = parse_curl_str(s)
    r = requests.post(url, data=data, headers=headers)
    return r


def assert_request_success(curl_str):
    """assert断言测试请求是否成功，"""
    response = request_curl_str(curl_str)
    if response.status_code != 200:
        pprint(parse_curl_str(curl_str))
    import ipdb; ipdb.set_trace()  # BREAKPOINT
    assert response.status_code == 200

    html = response.text
    o = json.loads(html)
    pprint(o)
    if o['ret'] != 0:
        pprint(parse_curl_str(curl_str))
    assert o['ret'] == 0    # return success


def get_file_curl_list(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


PAT = re.compile(r'ppysid="(.+)?"')    # ppysid这个cookie会过期，可以更新


def get_replace_cookie(curl_str, cookie=None):
    if cookie:
        return re.sub(PAT, 'ppysid="%s"'%cookie, curl_str)
    return curl_str


def get_replace_port(curl_str, port=None):
    if port:
        url, _, _ = parse_curl_str(curl_str)
        url_info = urlparse(url)
        netloc = url_info.netloc
        new_netloc = netloc.replace(str(url_info.port), str(port))
        return curl_str.replace(netloc, new_netloc)
    return curl_str


def assert_many_requests(curl_str_list, port=None, cookie=None):
    for curl_str in curl_str_list:
        curl_str = get_replace_cookie(curl_str, cookie=COOKIE)    # replace COOKIE
        curl_str = get_replace_port(curl_str, port=port)
        #print(curl_str)
        assert_request_success(curl_str)


if __name__ == '__main__':
    cookie = COOKIE = "PMs5bkeZejlwWIKw2D4ImFNnN0k/ANHaC9Wz/37nSTA="
    port = ''

    import sys
    try:
        filepath = sys.argv[1]
    except IndexError:
        exit()
    curl_str_list = get_file_curl_list(filepath)
    assert_many_requests(curl_str_list, port, cookie)
