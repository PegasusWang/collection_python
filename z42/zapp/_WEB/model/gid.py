#!/usr/bin/env python
#coding:utf-8
from _db import redis, R

R_GID = R.GID()

if not redis.exists(R_GID):
    redis.set(R_GID, 9912499)

def gid():
    return redis.incr(R_GID)

if __name__ == '__main__':
    print gid()
    #redis.set(R_GID, 9912499)
