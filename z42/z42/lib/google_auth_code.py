#!/usr/bin/env python
#coding:utf-8
import base64
import time
import struct
import hmac
import hashlib
from os import urandom

class GoogleAuthCode(object):
    '''谷歌二次认证,使用totp算法
    '''
    @classmethod
    def verify(cls, token, qrcode):
        '''查看code是否正确
        '''
        assert len(qrcode) == 6
        qrcode = int(qrcode)
        mscale = int(time.time()) / 30
        for i in xrange(-1, 2):
            if cls._new(token, mscale+i) == qrcode:
                return True
        return False

    @classmethod
    def create_token(cls):
        '''生成密钥:YIU4S8729D8DASJ3Y
        '''
        return base64.b32encode(urandom(15))

    @classmethod
    def _new(cls, token, mscale):
        '''六位数字:052821
        ref:http://stackoverflow.com/questions/8529265/google-authenticator-implementation-in-python
        '''
        token = base64.b32decode(token)
        mscale = struct.pack('>Q', mscale)
        tmp = hmac.new(token, mscale, digestmod=hashlib.sha1).digest()
        o = ord(tmp[19]) & 15
        base = struct.unpack('>I', tmp[o:o + 4])[0] & 0x7fffffff
        code = base % 1000000
        return code

    @classmethod
    def get(cls, token):
        return str(cls._new(token, int(time.time()) / 30)).zfill(6)


