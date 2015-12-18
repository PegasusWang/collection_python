#!/usr/bin/env python
#coding:utf-8
import _env
from urllib import urlencode
import urllib2
import logging
from z42.config import SMSBAO 

def sms_new(code, phone, txt):
    code = int(code)
    data = {
        'u': SMSBAO.USER,
        'p': SMSBAO.PASSWORD,
        'm': phone,
        'c': txt,
    }
    url = 'http://www.smsbao.com/sms?%s' % urlencode(data)
    urllib2.urlopen(url, timeout=60)

if __name__ == "__main__":
    pass
    sms_new("86", 13693622296 , "长生")
    sms_new("86", 18610542503 , "长生")
