#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
author: http://stackoverflow.com/users/476920/xperroni
"""


from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text


def main():
    text = r'''
Picasa工具箱Tool for Picasa Google+ Photo是目前最好的Picasa管理器，只是感觉Picasa有些过时了... <span style="color: #999">点评来自 <a
            href="/u/97100">@tastypear
    '''
    print(dehtml(text))


if __name__ == '__main__':
    main()
