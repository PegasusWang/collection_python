#!/usr/bin/env python
#coding:utf-8

from cgi import escape

def txt2html(s):
    s = escape(s)
    s = s.replace('\n', '</p><p>')
    return '<p>%s</p>'%s

