#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
chrome有个功能，对于请求可以直接右键copy as curl，然后在命令行里边用curl
模拟发送请求。现在需要把此curl字符串处理成requests库可以传入的参数格式，
http://stackoverflow.com/questions/23118249/whats-the-difference-between-request-payload-vs-form-data-as-seen-in-chrome
"""

import re
import sys
import pprint
import traceback
import requests
from functools import wraps
from pprint import pformat
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
    """convert chrome curl string to url, headers_dict and data
    js version http://curl.trillworks.com/
    """
    pat = re.compile("'(.*?)'")
    str_list = [i.strip() for i in re.split(pat, s)]   # 拆分curl请求字符串

    url = ''
    headers_dict = {}
    data = ''

    for i in range(0, len(str_list) - 1, 2):
        arg = str_list[i]
        string = str_list[i + 1]

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

        for i in range(0, len(str_list) - 1, 2):
            arg = str_list[i]
            string = str_list[i + 1]

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

    def print_py_code(self):
        print("""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

url = '{url}'

headers = {headers_dict}

params = {data_dict}

try:
    response = requests.request(
        method='GET',
        url=url,
        headers=headers,
        params=params,
    )
except BaseException:
    pass

print(response.status_code)
print(response.text)
    """.format(
            url=self.get_url(),
            headers_dict=pformat(self.get_headers_dict()),
            data_dict=pformat(self.get_data(as_dict=True))
        )
    )


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
    import os
    """change_ip use tor as socks proxy, this command can change tor ip"""
    os.system(
        """(echo authenticate '"%s"'; echo signal newnym; echo quit) | nc localhost 9051""" %
        CONFIG.CRAWLER.PROXIES_PASSWORD)
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
    import random
    import socket
    import struct
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))


def download_file(url, filename=None):
    """ requests 下载大文件 """
    local_filename = filename or url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


class Downloader(object):
    def __init__(self, url):
        self.url = url

    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs)

    def download_file(self, filename=None):
        local_filename = filename or self.url.split('/')[-1]
        r = self.get(self.url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return local_filename

    def get_content(self):
        # http://stackoverflow.com/questions/9718950/do-i-have-to-do-stringio-close
        r = self.get(self.url, stream=True)
        io = BytesIO()
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                io.write(chunk)
        return io.getvalue()


def class_method_decorator(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        method(self, *method_args, **method_kwargs)
    return _impl


def test():
    try:
        curl_str = """
        curl 'https://lens.example.com/api/videos' -H 'Origin: https://www.example.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' -H 'content-type: application/json' -H 'accept: application/json' -H 'Referer: https://www.example.com/question/60365400/answer/190921873' -H 'Cookie: d_c0="AJACuLlhmQuPTn2vsrcL9qGmFnpqP9IEKqE=|1492051835"; _zap=cc33b80e-7c35-45a0-b17d-08c6b31703a7; q_c1=c3b3eef99ea84f81b7a268e722582ce0|1496661480000|1493969643000; r_cap_id="NThlOWFiMDc0MDliNDcwN2JlNTY2YzExZTIzMDhiZGE=|1497859859|7a560fb57d9bbcdae5e48940f46659cee849bea3"; cap_id="YmMwN2NiMDkwMzI3NGFlMDk4MTFiMzc0MmMxMzY4Zjc=|1497859859|dad5613c0c66e163c7bd3b30f4072f2a0fa2db22"; z_c0=Mi4wQUlEQ21VY2N1Z3NBa0FLNHVXR1pDeGNBQUFCaEFsVk5HQlJ2V1FCdEdiV0Q0RVEtZnhXcXBkT3dyWGgtR2VyUnFR|1497859864|0eaff0ad45e32c8df7f3081376846bd582ba2f03; __utma=98467586.242125449.1492411107.1498457835.1498465254.3; __utmc=98467586; __utmz=98467586.1498465254.3.3.utmcsr=sentry.tc.example.com|utmccn=(referral)|utmcmd=referral|utmcct=/example/lens/issues/859/; aliyungf_tc=AQAAAHcqPAdoew4AJdbsaO5GrhzYQXjs; __utma=155987696.242125449.1492411107.1498735925.1499047670.5; __utmc=155987696; __utmz=155987696.1498617421.2.2.utmcsr=sentry.tc.example.com|utmccn=(referral)|utmcmd=referral|utmcct=/example/qaweb/issues/4575/; _ga=GA1.2.242125449.1492411107; _gid=GA1.2.378840776.1499046518; _xsrf=0e38bbb0c9bc4ced83da0a1a1c262538' -H 'Connection: keep-alive' -H 'x-upload-content-length: 390345' -H 'x-upload-content-type: video/mp4' --data-binary '{"use_watermark":true}' --compressed
        """
        #  curl_str = sys.argv[1]  # 用三引号括起来作为参数
        url, headers_dict, data = parse_curl_str(curl_str)
        pprint.pprint(headers_dict)
    except IndexError:
        exit(0)


if __name__ == '__main__':
    curl_str = """
    curl 'https://api.example.com/answers/193398779?with_pagination=1' -H 'Cache-Control: no-cache' -H 'Accept-Encoding: gzip' -H 'Authorization: Bearer 2.0AHAAe0WdQAoAMEIc8tUgDAwAAABgAlVNHimhWQCR4JzSn2B6kkVeOAzYk4Hw7A49Ug' -H 'Cookie: capsion_ticket=2|1:0|10:1501142008|14:capsion_ticket|44:N2JkNGFkODZkNjllNGFhZWFkMjY3YjQ5MTZhYzE3MTk=|9ef48d3b3ec3bb46662810eb46eeb29f9f8f82968b0ecc5c3efb812ef74e94e1; q_c1=d7851211ff714fa88b36def879c94fcc|1501141999000|1501141999000; z_c0=2|1:0|10:1501142046|4:z_c0|92:Mi4wQUhBQWUwV2RRQW9BTUVJYzh0VWdEQXdBQUFCZ0FsVk5IaW1oV1FDUjRKelNuMkI2a2tWZU9BellrNEh3N0E0OVVn|3b929cffaa14af19633ab747dd956078ce9644c6728a76942288797c2e6e1a7a; aliyungf_tc=AQAAAKEKozNfygYAAvTLb225pGtC7l17' -H 'User-Agent: Futureve/4.56.0-alpha Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 Google-HTTP-Java-Client/1.22.0 (gzip)' -H 'x-api-version: 3.0.62' -H 'x-app-version: 4.56.0-alpha' -H 'x-app-za: OS=Android&Release=7.1.1&Model=MI+6&VersionName=4.56.0-alpha&VersionCode=727155149&Width=1080&Height=1920&Installer=Dev&WebView=55.0.2883.91' -H 'x-app-build: release' -H 'x-network-type: WiFi' -H 'x-udid: ADBCHPLVIAxLBfqmzExvw6N1TrM-JpnRBjc=' -H 'Connection: Keep-Alive' --compressed
    """
    CurlStrParser(curl_str).print_py_code()
