#!/usr/bin/env python
#coding:utf-8
import _env
from _db import R,redis
from z42.config import HOST
from ob_cid import ObCid

_CID_BY_HOST_CACHE = (None, None)

HOST_SUFFIX = '.'+HOST
def cid_by_host(host):
    global _CID_BY_HOST_CACHE
    if host.endswith(HOST_SUFFIX):
        if host == _CID_BY_HOST_CACHE[0]:
            return _CID_BY_HOST_CACHE[1]
        else:
            host_id = host_id_by_host(host)
            cid = cid_by_host_id(host_id) if host_id else None
            _CID_BY_HOST_CACHE = (host, cid)
            return cid

def host_id_by_host(host):
    host_id = host.split('.', 1)[0]
    if host_id.isdigit():
        host_id = int(host_id)
        return host_id
    else:
        return id_by_host(host)

def cid_by_host_id(host_id):
    return ObCid.get(host_id) 

R_ID_HOST = R.ID_HOST()
R_HOST_ID = R.HOST_ID()

def id_host_new(id, host):
    with redis.pipeline() as p:
        p.hset(R_ID_HOST, id, host)
        p.hset(R_HOST_ID, host, id)
        p.execute()

def id_by_host(host):
    return redis.hincrby(R_HOST_ID, host, 0)

def host_by_id(id):
    return redis.hget(R_ID_HOST, id) or 0
    
if __name__ == "__main__":
#    print id_host_new(3,"test")
    print id_by_host("test")
