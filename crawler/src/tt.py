#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
chrome有个功能，对于请求可以直接右键copy as curl，然后在命令行里边用curl
模拟发送请求。现在需要把此curl字符串处理成requests库可以传入的参数格式，
http://stackoverflow.com/questions/23118249/whats-the-difference-between-request-payload-vs-form-data-as-seen-in-chrome
"""

import re
import traceback
import requests
from functools import wraps
from tld import get_tld    # pip install tld
try:
    from http.cookies import SimpleCookie
except ImportError:
    from Cookie import SimpleCookie
try:    # py3
    from urllib.parse import urlparse, quote, urlencode, unquote
    from urllib.request import urlopen
except ImportError:    # py2
    from urllib import urlencode, quote, unquote
    from urllib2 import urlopen


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


class CurlStrParser(object):
    def __init__(self, s):
        self.s = s

    def parse_curl_str(self, data_as_dict=False):
        s = self.s
        s = s.strip('\n').strip()
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

        if data_as_dict:
            data_dict = {}
            pair_list = unquote(data_str).split('&')
            for pair in pair_list:
                k, v = pair.split('=')
                data_dict[k] = v
            return url, headers_dict, data_dict
        else:
            return url, headers_dict, data_str

    def get_url(self):
        return self.parse_curl_str()[0]

    def get_headers_dict(self):
        return self.parse_curl_str()[1]

    def get_data(self, as_dict=False):
        return self.parse_curl_str()[2]


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
    headers = {'X-Forwarded-For': '192.155.212.33',
               'REMOTE_ADDR': '192.155.212.4',
               'X-Real-Ip': '192.155.323.4'}
    return requests.get(url, headers=headers).text
    #return requests.get(url).text


def form_data_to_dict(s):
    """form_data_to_dict s是从chrome里边复制得到的form-data表单里的字符串，
    注意*必须*用原始字符串r""

    :param s: form-data string
    """
    arg_list = [line.strip() for line in s.split('\n')]
    d = {}
    for i in arg_list:
        if i:
            k = i.split(':', 1)[0].strip()
            v = ''.join(i.split(':', 1)[1:]).strip()
            d[k] = v
    return d


def change_ip():
    """change_ip use tor as socks proxy, this command can change tor ip"""
    os.system("""(echo authenticate '"%s"'; echo signal newnym; echo quit) | nc localhost 9051"""%CONFIG.CRAWLER.PROXIES_PASSWORD)
    print(my_ip())


def get_domain(url):
    return get_tld(url)


def cookie_dict_from_cookie_str(cookie_str):
    """cookie_dict_from_str Cookie字符串返回成dict

    :param cookie_str: cookies string
    """
    cookie = SimpleCookie()
    cookie.load(cookie_str)
    return {key: morsel.value for key, morsel in cookie.items()}


def cookie_dict_from_response(r):
    """cookie_dict_from_response 获取返回的response对象的Set-Cookie字符串
    并返回成dict

    :param r: requests.models.Response
    """
    cookie_str = r.headers.get('Set-Cookie')
    return cookie_dict_from_cookie_str(cookie_str)


def get_proxy_dict(ip, port, proxy_type='http' or 'socks5'):
    """get_proxy_dict return dict proxies as requests proxies
    http://docs.python-requests.org/en/master/user/advanced/

    :param ip: ip string
    :param port: int port
    :param proxy_type: 'http' or 'socks5'
    """
    proxies = {
        'http': '{proxy_type}://{ip}:{port}'.format(proxy_type=proxy_type, ip=ip, port=port),
        'https': '{proxy_type}://{ip}:{port}'.format(proxy_type=proxy_type, ip=ip, port=port),
    }
    return proxies


def random_ip():
    import random, socket, struct
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))


if __name__ == '__main__':


    url = 'http://182.92.196.13:8000/ip'
    headers = {'X-Forwarded-For': '192.155.212.33',
               'REMOTE_ADDR': '192.155.212.4',
               'X-Real-Ip': '192.155.323.4'}
    print requests.get(url, headers=headers).text

    url = 'http://httpbin.org/ip'
    headers = {'X-Forwarded-For': '192.155.212.33',
               'REMOTE_ADDR': '192.155.212.4',
               'X-Real-Ip': '192.155.323.4'}
    print requests.get(url, headers=headers).text


    url = 'https://api.ipify.org?format=json'
    headers = {'X-Forwarded-For': '192.155.212.33',
               'REMOTE_ADDR': '192.155.212.4',
               'X-Real-Ip': '192.155.323.4'}
    print requests.get(url, headers=headers).text
