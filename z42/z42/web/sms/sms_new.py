#!/usr/bin/env python
#coding:utf-8
from smsbao import sms_new as smsbao_new

def sms_new(code, phone, txt):
    if isinstance(code,basestring) and not code.isdigit():
        return
    code = int(code)
    if code == 86:
        _new = smsbao_new
    else:
        from sms_twilio import sms_new as sms_twilio_new
        _new = sms_twilio_new 
    #print code, phone
    _new(code, phone, txt)
