#!/usr/bin/env python
#coding:utf-8

from _db import redis, R
from zapp._WEB.model.ob import Ob
from os import urandom
from struct import pack, unpack
import binascii
from base64 import urlsafe_b64encode, urlsafe_b64decode

R_SESSION = R.SESSION('%s')

class Session(object):
    @classmethod
    def get(cls, user_id):
        key = R_SESSION%user_id
        return redis.get(key)

    EXPIRE_DAY = 365


    @classmethod
    def id_by_b64(cls, session):
        id, binary = _id_binary_decode(session)
        if id:
            key = R_SESSION%id
            id = int(id)
            if id and binary and binary == redis.get(key):
                return id

    @classmethod
    def new(cls, id, expire=EXPIRE_DAY*3600*24):
        id = int(id)
        if id:
            s = cls.get(id) or urandom(12)
            cls.set(id, s)
            return cls.encode(id, s) 

    @classmethod
    def set(cls, id, session, expire=EXPIRE_DAY*3600*24):
        key = R_SESSION%id
        redis.setex(key, expire, session)
        return cls.encode(id, session)

    @classmethod
    def rm(cls, id):
        redis.delete(R_SESSION%id)

    @classmethod
    def decode(cls, session, verify=True):   
        id, binary = _id_binary_decode(str(session))
        if id:
            id = int(id)
            if id and binary:
                if verify:
                    if binary == cls.get(id):
                        return id
                else:
                    return id, binary
                    
    @classmethod
    def encode(cls, id, session):
        ck_key = urlsafe_b64encode(session)
        return '%s.%s' % (id, ck_key)

def _id_binary_decode(session):
    if not session:
        return None, None
    id, value = session.split('.', 1)
    try:
        value = urlsafe_b64decode(value+"==")
    except (binascii.Error, TypeError):
        return None, None
    id = int(id)
    return id, value



if __name__ == '__main__':
#    s = Session.new(1)
#    print Session.id_by_b64(s)
    print Session.decode("9912501.whphyNQ_5m5yCEaN", True)
    print Session.decode("9912501.whphyNQ_5m5yCEaN", True)
    #9912501.whphyNQ_5m5yCEaN


