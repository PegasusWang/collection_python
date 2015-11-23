#!/usr/bin/env python
# -*- coding:utf-8 -*-


from bs4 import BeautifulSoup
def html2txt(html=u''):
    print html
    soup = BeautifulSoup(html)
    print soup.get_text()


from html2text import html2text    # to markdown not plain text
def html2makrdown(html=u''):
    markdown = html2text(html)
    return markdown


import re
def remove_html_tags(html=u''):
    TAG_RE = re.compile(r'<[^>]+>')
    def remove_tags(text):
        return TAG_RE.sub('', text)

import xml.etree
def remove_html_tags(text):
    return ''.join(xml.etree.ElementTree.fromstring(text).itertext())
