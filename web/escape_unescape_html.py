#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
import cgi
s = cgi.escape( """& < >""" )   # s = "&amp; &lt; &gt;"

import HTMLParser
h = HTMLParser.HTMLParser()
print h.unescape('&pound;682m')
'''


def escape_html(html):
    import cgi
    return cgi.escape(html)


def unescape_html(html):
    import HTMLParser
    return HTMLParser.HTMLParser().unescape(html)

# from xml.sax.saxutils import escape, unescape
print(escape_html('<p>hehe</p>'))
