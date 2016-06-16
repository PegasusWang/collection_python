# -*- coding: utf-8 -*-

from lxml import etree
import requests


def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


class XpathCrawler(object):
    def __init__(self, url, xpath_dict):
        self.url = url
        self.xpath_dict = xpath_dict

    @lazy_property
    def html(self):
        """
        :return: html unicode text
        """
        return requests.get(self.url).text

    @lazy_property
    def parser(self):
        return etree.HTML(self.html)

    def save(self):
        pass

    def run(self):
        pass


class TaobaoCrawler(XpathCrawler):
    def get_title(self):
        title_xpath = self.xpath_dict.get('title')
        res = self.parser.xpath(title_xpath)[0].text.strip()
        print(len(res))
        return res


if __name__ == '__main__':
    url = 'https://item.taobao.com/item.htm?spm=a230r.7195193.1997079397.29.BC4BEb&id=525723102855&abbucket=15'
    d = {
        'availability': '',
        'condition': '',
        'description': '',
        'image_link': '',
        'link': '',
        'title': """//*[@id="J_Title"]/h3""",
        'price': '',
        'brand': '',
        'sale_price': '',
    }
    c = TaobaoCrawler(url, d)
    print(c.get_title())
