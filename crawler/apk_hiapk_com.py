#!/usr/bin/env python
# -*- coding:utf-8 -*-

import _env
import requests
import traceback
import time
from extract import extract, extract_all


class ApkSpider(object):
    def __init__(self, db):
        self._db = db

    def fetch(self, url):
        try:
            html = requests.get(url).text
        except:
            html = ''
            traceback.print_exc()
        return html

    def get_app_url_list(self, url):
        """url = http://apk.hiapk.com/apps?sort=5&pi=3
           loop pi
        """
        html = self.fetch(url)
        base_url = 'http://apk.hiapk.com'
        ul = extract('<ul id="appSoftListBox">', '</ul>', html)
        url_set = set()
        for i in extract_all('<a href="', '">', ul):
            url_set.add(i)
        res = [base_url+i for i in url_set if 'info' in i]
        return res

    def get_app_data_dict(self, url):
        html = self.fetch(url)
        data = {}

        name = extract('<div id="appSoftName" class="detail_title left">',
                       '</div', html)
        name = name.split('(')[0]
        detail = extract('<div class="detail_right">', '</div>', html)
        tag = extract('<a class="detail_right_type"',  '</a>', html)
        tag = extract('<span class="font14">', '</span>', tag)
        brief = extract('<pre id="softIntroduce">', '</pre>', html)
        company = extract('<span class="d_u_line">', '</span>', html)
        hot_count = extract_all('<span class="font14">', '</span>', html)
        hot_count = hot_count[1]
        logo = extract('<img width="72" height="72" src="', '"', html)

        data = dict(name=name, tag=tag, brief=brief, company=company,
                    hot_count=hot_count, logo=logo)
        return data

    def save(self, app_data):
        """data is app info dict """
        self._db.write_point(
            {
                "measurement": "app",
                "tags": {
                    "name": app_data.get('name'),
                },
                "time": int(time()*1000000000),
                "fields": {
                    'name': app_data.get('name'),
                    'tag': app_data.get('tag'),
                    'brief': app_data.get('brief'),
                    'company': app_data.get('company'),
                    'hot_count': app_data.get('hot_count'),
                }
            }
        )


def test():
    DB = ''
    page = 1
    base_url = 'http://apk.hiapk.com/apps?sort=5&pi='
    s = ApkSpider(DB)
    for i in range(1, page+1):
        url = base_url + str(page)
        app_data_url_list = s.get_app_url_list(url)

        app_data_list = []
        for app_url in app_data_url_list:
            app_data_list.append(s.get_app_data_dict(app_url))

        for app_data in app_data_list:
            for k, v in app_data.iteritems():
                print k, v
            print '\n\n************\n\n'


def main():
    DB = ''
    page = 10
    base_url = 'http://apk.hiapk.com/apps?sort=5&pi='
    s = ApkSpider(DB)
    for i in range(1, page+1):
        url = base_url + str(page)
        app_data_url_list = s.get_app_url_list(url)

        app_data_list = []
        for app_url in app_data_url_list:
            app_data_list.append(s.get_app_data_dict(app_url))

        for app_data in app_data_list:
            s.save(app_data)


if __name__ == '__main__':
    #main()
    test()
