#!/usr/bin/env python
# -*- coding:utf-8 -*-


# method 1
from bs4 import BeautifulSoup
html = None


def html2txt(html=''):
    print html
    soup = BeautifulSoup(html)
    print soup.get_text()


# method 2
from html2text import html2text

def html2makrdown(html=''):
    html2text(html)
