#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
chrome有个功能，对于请求可以直接右键copy as curl，然后在命令行里边用curl
模拟发送请求。现在需要把此curl字符串处理成requests库可以传入的参数格式，
用python脚本更好的进行模拟。可以用来发广告机器人
暂时测试网址：tech2ipo.com; liwushuo.com
http://stackoverflow.com/questions/23118249/whats-the-difference-between-request-payload-vs-form-data-as-seen-in-chrome
"""

import re
import requests
# http://python-future.org/compatible_idioms.html
try:   # py3
    from urllib.parse import urlparse, urlencode, unquote
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:    # py2
    from urlparse import urlparse
    from urllib import urlencode, unquote
    from urllib2 import urlopen, Request, HTTPError


tech2ipo_str = """
curl 'https://cn.avoscloud.com/1.1/functions/PostTxt.new' -H 'origin: http://tech2ipo.com' -H 'accept-encoding: gzip, deflate' -H 'accept-language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'content-type: text/plain' -H 'accept: */*' -H 'referer: http://tech2ipo.com/10026690' --data-binary $'{"post_id":"5685139100b01b9f2be8e5ab","txt":"\u5bb6\u5ead\u6559\u80b2","_ApplicationId":"qatav4vek3wbpsidrv867us5ootbnkxt9l1pw7ppz16rrfzc","_ApplicationKey":"zio0z5lb0mramk7z6akn7dakmw2bb015s3r8d4e9izqnmveq","_ApplicationProduction":0,"_ClientVersion":"js0.5.4","_InstallationId":"f83f19ae-e110-1bf0-df0b-e069607a0e29","_SessionToken":"e7wsvkygs3mrewz8ssumql9vj"}' --compressed
"""

#liwushuo_str = """curl 'http://www.liwushuo.com/api/posts/1022318/comments' -H 'Cookie: next_url=http://www.liwushuo.com/; _gat=1; session=6fa80dcf-af05-49ea-a935-18d455eb29f6; Hm_lvt_8a996f7888dea2ea6d5611cd24318338=1452052061,1452136889,1452138175,1452138280; Hm_lpvt_8a996f7888dea2ea6d5611cd24318338=1452158617; _ga=GA1.3.477073430.1452046529' -H 'X-NewRelic-ID: UQQAUlFTGwQBUFBRAQQ=' -H 'Origin: http://www.liwushuo.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://www.liwushuo.com/posts/1022318' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'content=beautiful' --compressed"""
liwushuo_str = """curl 'http://www.liwushuo.com/api/posts/1030667/comments' -H 'Cookie: _gat=1; next_url=http://www.liwushuo.com/; session=6fa80dcf-af05-49ea-a935-18d455eb29f6; post_1030667=true; _ga=GA1.3.477073430.1452046529; Hm_lvt_8a996f7888dea2ea6d5611cd24318338=1452052061,1452136889,1452138175,1452138280; Hm_lpvt_8a996f7888dea2ea6d5611cd24318338=1452329576' -H 'X-NewRelic-ID: UQQAUlFTGwQBUFBRAQQ=' -H 'Origin: http://www.liwushuo.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://www.liwushuo.com/posts/1030667' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'content=%E8%AF%84%E8%AE%BA' --compressed"""


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


def parse_curl_str(s, data_as_dict=False):
    """Convert chrome curl string to url, headers dict and data string
    此函数用来作为单元测试中提交按钮的操作
    :param s: 右键chrome请求点击copy as curl得到的字符串。
    :param data_as_dict: if True, return data as dict
    """
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
        if not data_str:
            return url, headers_dict, {}
        data_dict = {}
        pair_list = unquote(data_str).split('&')
        for pair in pair_list:
            k, v = pair.split('=')
            data_dict[k] = v
        return url, headers_dict, data_dict
    else:
        return url, headers_dict, data_str


def request_curl_str(s):
    url, headers, data = parse_curl_str(s)
    r = requests.post(url, data=data, headers=headers)
    return r


'''
if __name__ == '__main__':
    def test_liwushuo():
        url, headers, data = parse_curl_str(liwushuo_str)
        # data = urlencode([tuple('content=requests测试'.split('='))])
        data_str = 'content=真心好'
        data = urlencode(encode_to_dict(data_str))
        r = requests.post(url, data=data, headers=headers)
        print(r.content)

    #test_liwushuo()


    def test_tech2ipo():
        url, headers, data = parse_curl_str(tech2ipo_str)
        r = requests.post(url, json=json.loads(data), headers=headers)  # loads
        print(r.content)

    #test_tech2ipo()


    def test_lagou():
        lagou_str = """curl 'http://www.lagou.com/jobs/positionAjax.json?gj=1-3%E5%B9%B4&px=default&city=%E5%8C%97%E4%BA%AC' -H 'Cookie: user_trace_token=20150911115414-e35eaafdf3cd430fb0a9fed4ca568273; LGUID=20150911115415-c53a987d-5838-11e5-8fa5-525400f775ce; fromsite=www.baidu.com; LGMOID=20160112143105-A2EDC0F26EF4FF9F7A0E261E95FFC0D5; tencentSig=5171360768; JSESSIONID=0F7B9502EFBBC658FD043C42196C5F58; PRE_UTM=; PRE_HOST=; PRE_SITE=http%3A%2F%2Fwww.lagou.com%2Fjobs%2F1018226.html; PRE_LAND=http%3A%2F%2Fwww.lagou.com%2Fjobs%2F1018226.html; login=true; unick=%E7%8E%8B%E5%AE%81%E5%AE%81-Python%E5%BA%94%E8%81%98; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=77; SEARCH_ID=c70df91703ee4c1ca380d883e93dde6c; index_location_city=%E5%8C%97%E4%BA%AC; _gat=1; HISTORY_POSITION=1326282%2C9k-18k%2C%E4%BB%80%E4%B9%88%E5%80%BC%E5%BE%97%E4%B9%B0%2CPython%7C1247829%2C8k-16k%2CPair%2CPython%7C1162119%2C8k-15k%2C%E5%A4%A7%E7%A0%81%E7%BE%8E%E8%A1%A3%2CPython%E5%B7%A5%E7%A8%8B%E5%B8%88%7C411250%2C10k-20k%2C%E6%9C%89%E5%BA%B7%E7%88%B1%E5%B8%AE%2CPython%20%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88%7C1269616%2C12k-20k%2CE%E7%98%A6%E7%BD%91%2CPython%7C; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1452172939,1452231058,1452231062,1452580269; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1453095567; LGSID=20160118132416-b7c3fc3c-bda3-11e5-8bf5-5254005c3644; LGRID=20160118133926-d61df46a-bda5-11e5-8a39-525400f775ce; _ga=GA1.2.878965075.1441943655' -H 'Origin: http://www.lagou.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://www.lagou.com/jobs/list_Python?gj=1-3%E5%B9%B4&px=default&city=%E5%8C%97%E4%BA%AC' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'first=false&pn=9&kd=Python' --compressed"""
        url, headers, data = parse_curl_str(lagou_str)
        r = requests.post(url, data=data, headers=headers)  # loads
        print(r.content)

    def test_sougou_wechat():
        s = """curl 'http://weixin.sogou.com/gzhjs?openid=oIWsFt1XTuB0RIm7PjTHp51TNhqs&page=12' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: SUV=00A27B2BB73D015554D9EC5137A6D159; ssuid=6215908745; SUID=2E0D8FDB66CA0D0A0000000055323CAB; usid=g6pDWznVhdOwAWDb; CXID=9621B02E3A96A6AB3F34DB9257660015; SMYUV=1448346711521049; _ga=GA1.2.1632917054.1453002662; ABTEST=8|1455514045|v1; weixinIndexVisited=1; ad=G7iNtZllll2QZQvQlllllVbxBJtlllllNsFMpkllllUlllllRTDll5@@@@@@@@@@; SNUID=C1B8F6463A3F10F2A42630AD3BA7E3E1; sct=1; ppinf=5|1455520623|1456730223|Y2xpZW50aWQ6NDoyMDE3fGNydDoxMDoxNDU1NTIwNjIzfHJlZm5pY2s6NzpQZWdhc3VzfHRydXN0OjE6MXx1c2VyaWQ6NDQ6NENDQTE0NDVEMTg4OTRCMTY1MUEwMENDQUNEMEQxNThAcXEuc29odS5jb218dW5pcW5hbWU6NzpQZWdhc3VzfA; pprdig=Xmd5TMLPOARs3V2jIAZo-5UJDINIE0oFY97uU510_JOZm2-uu5TnST5KKW3oDgJY6-xd66wDhsb4Nm8wbOh1FCPohYO12b1kCrFoe-WUPrvg9JSqC72rjagjOlDg-JX72LcIjFOhsj7l_YGuaJpDrjFPoqy39C0AReCpmVcI5SM; ppmdig=1455520623000000ff71eef01ec88b2fe45bfa15b36e3532; IPLOC=CN' -H 'Connection: keep-alive' --compressed"""
        url, headers, data = parse_curl_str(s)
        url = 'http://weixin.sogou.com/weixin?type=1&query=内涵段子'
        url = 'http://weixin.sogou.com/gzhjs?openid=oIWsFt1XTuB0RIm7PjTHp51TNhqs&page=12'
        r = requests.get(url, headers=headers)
        print(r.text)

    test_sougou_wechat()
'''


if __name__ == '__main__':
    import sys
    from pprint import pprint
    try:
        curl_str = sys.argv[1]
        url, headers, data = parse_curl_str(curl_str, True)
        print(url)
        pprint(headers)
        print(headers['User-Agent'])
        print(data)
    except IndexError:
        pass
