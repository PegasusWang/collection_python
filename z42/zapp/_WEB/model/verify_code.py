#!/usr/bin/env python
# coding:utf-8
import _env
from msgpack import dumps, loads
from urllib import urlencode
from hashlib import sha256
from base64 import urlsafe_b64encode, urlsafe_b64decode
# print len(sha3_256("x").digest()) = 32


class VerifyCode(object):

    @classmethod
    def encode(cls, secret, data):
        o = dumps(data)
        sign = sha256(secret + o).digest()
        return urlsafe_b64encode(sign+o).rstrip('=')

    @classmethod
    def decode(cls, secret, data):
        if type(data) is unicode:
            data = str(data)
        data = urlsafe_b64decode(data + '==')
        sign = data[:32]
        o = data[32:]
        if sha256(secret+o).digest() == sign:
            return loads(o)


if __name__ == '__main__':
    print urlsafe_b64decode("2J2tNuziU3qMdgeF9JMIXzt3h66M4lQeGAuVFfa-z2GBpG1haWyoenNAZy5jb20"+"==")
    print urlsafe_b64decode("2J2tNuziU3qMdgeF9JMIXzt3h66M4lQeGAuVFfa-z2GBpG1haWyoenNAZy5jb20"+"==")
