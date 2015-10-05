#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..crawler import Spider
from bs4 import BeautifulSoup


class GifakSpider(Spider):

    def get_gif(self, url='http://gifak-net.tumblr.com'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        div_list = soup.find_all('div', class_='article-content')
        img_list = [i.find('img') for i in div_list if i]
        url_list = [i.get('src') for i in img_list if i]
        return url_list


class TumblrForgifsSpider(Spider):

    def get_gif(self, url='http://tumblr.forgifs.com/'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        media_list = soup.find_all('div', class_='media')
        img_list = [i.find('img') for i in media_list if i]
        url_list = [i.get('src') for i in img_list if i]
        return url_list


class GifsboomSpider(Spider):

    def get_gif(self, url='http://gifsboom.net'):
        self.url = url
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        img_tag_list = soup.find_all('img')
        img_list = [i.get('src') for i in img_tag_list if i]
        url_list = [i for i in img_list if '.gif' in i]
        return url_list


class GifsonSpider(Spider):
    def get_gif(self, url='http://gifson.net'):
        s = GifsboomSpider()
        return s.get_gif(url)


class LolgifruSpider(Spider):
    def get_gif(self, url='http://lolgif.ru'):
        s = GifsboomSpider()
        return s.get_gif(url)


class ElmontajistaSpider(Spider):
    """from 1 to 380 page"""
    def get_gif(self, url='http://elmontajista.tumblr.com'):
        s = GifsboomSpider()
        return s.get_gif(url)


class IcachondeoSpider(Spider):
    def get_gif(self, url='http://icachondeo.com/category/gifsanimados/'):
        s = GifsboomSpider()
        return s.get_gif(url)


class AewaeSpider(Spider):
    def get_gif(self, url='http://www.aewae.com/'):
        s = GifsboomSpider()
        return s.get_gif(url)


class TychoonSpider(Spider):
    def get_gif(self, url='http://tychoon.tumblr.com/'):
        s = GifsboomSpider()
        return s.get_gif(url)


class GaoxiaogifSpider(Spider):
    pass

