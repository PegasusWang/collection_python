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


class HotgirlsfcSpider(Spider):

    def get_img(self, url='http://hotgirlsfc.tumblr.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        media_list = soup.find_all('div', class_='img')
        img_list = [i.find('img') for i in media_list if i]
        url_list = [i.get('src') for i in img_list if i]
        return set(url_list)


class MzituSpider(Spider):

    def get_img(self, url='http://www.mzitu.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        img_list = soup.find_all('img', class_='lazy')
        url_list = [i.get('data-original') for i in img_list if i]
        return set(url_list)


class LovelyasiansSpider(Spider):
    def get_img(self, url='http://lovely-asians.tumblr.com'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        img_list = soup.find_all('img')
        url_list = [i.get('src') for i in img_list if i]
        url_list = [i for i in url_list if 'media.tumblr' in i]
        return set(url_list)


class KormodelsSpider(Spider):
    def get_post_img_list(self, url):
        """fetch http://kormodels.tumblr.com/post page"""
        print 'fetch...post', url
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'lxml')
        img_tag_list = soup.find_all('meta', attrs={'property': 'og:image'})
        url_list = [i.get('content') for i in img_tag_list if i]
        return set(url_list)

    def get_gif(self, url='http://kormodels.tumblr.com/tagged/gifs/'):
        url_list = self.get_img(url)
        url_list = [i for i in url_list if 'gif' in i]
        return url_list

    def get_img(self, url='http://kormodels.tumblr.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        a_tag_list = soup.find_all('a')
        href_list = [i.get('href') for i in a_tag_list if i]
        href_list = [i for i in href_list if 'kormodels.tumblr.com/post' in i]
        url_list = []
        for each in set(href_list):
            time.sleep(2)
            img_list = self.get_post_img_list(each)
            url_list.extend(list(img_list))
        return set(url_list)


class FerchoechoSpider(Spider):
    def get_img(self, url='http://ferchoecho.tumblr.com'):
        url_list = list(get_media_url_list(url))
        return [i for i in url_list if 'media.tumblr' in i]


class Girl2chickSpider(Spider):
    def get_img(self, url='http://girl2chick.tumblr.com/'):
        url_list = list(get_media_url_list(url))
        return [i for i in url_list if 'media.tumblr' in i]


class KoreangirlshdSpider(Spider):
    def get_img(self, url='http://koreangirlshd.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        post_tag_list = soup.find_all('div', class_='entry-content')
        img_tag_list = [i.find('img') for i in post_tag_list if i]
        a_list = [i.find('a') for i in post_tag_list if i]
        url_list = [i.get('src') for i in img_tag_list if i]
        href_list = [i.get('href') for i in a_list if i]
        for each in set(href_list):
            time.sleep(1)
            url_list.extend(list(get_media_url_list(each)))

        return set(url_list)



class SnsdpicsSpider(Spider):
    def get_img(self, url='http://snsdpics.com'):    # /page/n
        s = KoreangirlshdSpider()
        return s.get_img(url)
