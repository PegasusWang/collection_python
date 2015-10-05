#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..crawler import Spider
import requests
from bs4 import BeautifulSoup
import traceback
import lxml
from StringIO import StringIO
import time


class JiandanSpider(Spider):

    def get_meizi(self, url='http://jandan.net/ooxx/page-160010#comments'):
        "http://jandan.net/ooxx/page-%#comments, from 900 to 1496"
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        img_tag_list = soup.find_all('img')
        img_url_list = [i.get('src') for i in img_tag_list]
        return img_url_list

    def get_wuliao(self, url='http://jandan.net/pic/page-100010#comments'):
        "http://jandan.net/pic/page-%s#comments, from 4000 to 7058"
        return self.get_meizi(url)


def test_meizi():
    for i in range(900, 903):
        time.sleep(1)
        url = "http://jandan.net/ooxx/page-%s#comments" % str(i)
        print url
        s = JiandanSpider(url)
        html = s.get_html()
        img_list = s.get_meizi(html)
        for i in img_list:
            print i
            filename = i.rsplit('/')[-1]
            #with open(filename, 'wb') as f:
                #f.write(requests.get(i).content)


def test_wuliao():
    for i in range(4000, 4001):
        url = "http://jandan.net/pic/page-%s#comments" % str(i)
        print url
        s = JiandanSpider(url)
        html = s.get_html()
        img_list = s.get_wuliao(html)
        for i in img_list:
            filename = i.rsplit('/')[-1]
            print filename
            with open(filename, 'wb') as f:
                f.write(requests.get(i).content)


def test_all():
    cookies = '757477302=453; bad-click-load=off; nsfw-click-load=off; gif-click-load=off; _gat=1; 757477302=433; _ga=GA1.2.784043191.1438269751; Hm_lvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1438270942,1438270944,1438270947,1438995506; Hm_lpvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1439110556'
    s = JiandanSpider('', cookies)
    meizi_list = s.get_meizi()
    for each in meizi_list:
        print each
    wuliao_list = s.get_wuliao()
    for each in wuliao_list:
        print each


if __name__ == '__main__':
    test_all()
