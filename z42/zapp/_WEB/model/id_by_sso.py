#!/usr/bin/env python
# coding:utf-8
import _env
from zapp._WEB.model._db import redis, R
from zapp._WEB.model.gid import gid


R_ID_BY_SSO_ID = R.ID_BY_SSO_ID()
R_SSO_ID_BY_ID = R.SSO_ID_BY_ID()

def id_by_sso_id(id):
    _id = redis.hget(R_ID_BY_SSO_ID, id)
    if not _id:
        _id = gid()
        with redis.pipeline() as p:
            p.hset(R_ID_BY_SSO_ID, id, _id)
            p.hset(R_SSO_ID_BY_ID, _id, id)
            p.execute()
    return int(_id)


def sso_id_by_id(id):
    return int(redis.hget(R_SSO_ID_BY_ID, id) or 0)

if __name__ == '__main__':
    print redis.hgetall(R_SSO_ID_BY_ID)
