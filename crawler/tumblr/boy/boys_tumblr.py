#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..crawler import Spider
from bs4 import BeautifulSoup
import lxml
import requests
import time


# for recursive fetch
def fetch_html(url, retries=5):
    try:
        html = requests.get(url, timeout=20).text
    except:
        if retries > 0:
            print 'fetching...', retries, url
            time.sleep(3)
            return fetch_html(url, retries-1)
        else:
            print 'fetch failed', url
            return ''
    return html


def get_media_url_list(url):
    if not url:
        return []
    print 'fetch html...', url
    html = fetch_html(url)
    if not html:
        return []
    soup = BeautifulSoup(html, 'lxml')
    img_tag_list = soup.find_all('img')
    url_list = [i.get('src') for i in img_tag_list if i]
    return set(url_list)

"""
class HotgirlsfcSpider(Spider):

    def get_img(self, url='http://hotgirlsfc.tumblr.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        media_list = soup.find_all('div', class_='img')
        img_list = [i.find('img') for i in media_list if i]
        url_list = [i.get('src') for i in img_list if i]
        return set(url_list)
"""


class AllboysboysSpider(Spider):
    def get_img(self, url='http://allboysboys.tumblr.com/'):
        img_list = list(get_media_url_list(url))
        img_list = [i for i in img_list if 'media.tumblr' in i]
        return img_list


class LobbuSpider(Spider):
    def get_img(self, url='http://lobbu-lobbu.tumblr.com/'):
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'lxml')
        iframe_tag_list = soup.find_all('iframe')
        src_list = [i.get('src') for i in iframe_tag_list if i]
        img_list = list(get_media_url_list(url))
        for each_url in set(src_list):
            time.sleep(2)
            l = list(get_media_url_list(each_url))
            img_list.extend(l)
        img_list = [i for i in img_list if 'media' in i]
        return img_list
