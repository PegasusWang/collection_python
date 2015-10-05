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


class AnimalGifHunterSpider(Spider):
    def get_post_img_list(self, url):
        print 'fetch post...', url
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'lxml')
        img_tag_list = soup.find_all('meta', attrs={'property': 'og:image'})
        url_list = [i.get('content') for i in img_tag_list if i]
        return set(url_list)

    def get_img(self, url='http://animal-gif-hunter.tumblr.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        a_tag_list = soup.find_all('a')
        href_list = [i.get('href') for i in a_tag_list if i]
        href_list = [i for i in href_list if i and 'post' in i]
        url_list = []
        for each in set(href_list):
            time.sleep(2)
            img_list = self.get_post_img_list(each)
            url_list.extend(list(img_list))
        return set(url_list)



class  AlthingscuteSpider(Spider):
    def get_img(self, url='http://althingscute.tumblr.com/'):
        url_list = list(get_media_url_list(url))
        return [i for i in url_list if 'media.tumblr' in i]


class JunkuploadSpider(Spider):
    def get_img(self, url='http://junkupload.tumblr.com/'):
        url_list = list(get_media_url_list(url))
        return [i for i in url_list if 'media.tumblr' in i]


class CatsdogsblogSpider(Spider):
    """4247"""
    def get_img(self, url='http://catsdogsblog.com'):
        url_list = list(get_media_url_list(url))
        return [i for i in url_list if 'media.tumblr' in i]

class AnimalspatronusgifsSpider(Spider):
    def get_img(self, url='http://animalspatronusgifs.tumblr.com'):
        url_list = list(get_media_url_list(url))
        return [i for i in url_list if 'media.tumblr' in i]

