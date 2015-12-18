#!/usr/bin/env python
#coding:utf-8

from twilio.rest import TwilioRestClient
from z42.config import TWILIO


client = TwilioRestClient(TWILIO.SID, TWILIO.TOKEN)

def sms_new(code, phone, txt):
    code = int(code)
    if code:
        number = "+%s%s"%(code,phone)
    else:
        number = str(phone)
    try:
        message = client.sms.messages.create(to=number, from_="+14698888422", body=txt)
    except:
        print code, phone
if __name__ == "__main__":

    code = 1 
    phone = 3234384088
    sms_new(code, phone, "中国@北京") 
