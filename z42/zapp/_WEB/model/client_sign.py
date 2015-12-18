#!/usr/bin/env python
# coding:utf-8
import _env
from hashlib import sha512
from base64 import urlsafe_b64encode, urlsafe_b64decode
from zapp._WEB.model.session import Session
from time import time as _time
from json import dumps
from urllib import urlencode

class ClientSign(object):

    @classmethod
    def verify(cls, sign, secret, o, time):
        sign = urlsafe_b64decode(sign + "==")
        if sign == cls.sign(secret, o, time):
            return True

    @classmethod
    def sign(cls, secret, o, time):
        return sha512("%s|%s|%d" % (secret, o, time)).digest()

    @classmethod
    def url(cls, secret, o):
        o = dumps(o)
        time = int(_time())

        sign = urlsafe_b64encode(
            cls.sign(secret, o, time)
        ).rstrip("=")
        s = "%d|%s" % (time, sign)
        return urlencode(dict(
            s=s,
            o=o
        ))

if __name__ == "__main__":
    secret = "322"

    time = 1413355462
    sign = "TgmMu9pvaODyHSvpQWj_M57LoxYIDa2IDZ2tf-n33805kwkVZfY8iogE8_fyeKbaGSAL3GcyzsJRh_dkf1rfAA"
    o = "[3, 32, 4425]"

    print Sign.url(secret, [3, 32, 4425])
    print Sign.verify(sign, secret, o, time)
