#!/usr/bin/env python
# coding:utf-8
import _env
from zapp._WEB.model._db import redis, R
from time import time

R_STAR_COUNT = R.STAR_COUNT()  # HSET , 我们保证id和user_id不会出现相同的

R_STAR_BY_ID = R.STAR_BY_ID('%s')  # ZSET
R_STAR_BY_USER_ID_CID = R.STAR_BY_USER_ID_CID('%s_%s')  # ZSET


class Star(object):

    @staticmethod
    def set(user_id, id, cid, action):
        action = int(action)
        if action:
            Star.new(user_id, id, cid)
        else:
            Star.rm(user_id, id, cid)

    @classmethod
    def new(cls, user_id, id, cid):
        key = R_STAR_BY_USER_ID_CID % (user_id, 0)
        if redis.zrank(key, id) is None:
            _now = int(time())
            with redis.pipeline() as p:
                p.hincrby(R_STAR_COUNT, user_id)
                p.hincrby(R_STAR_COUNT, id)
                p.zadd(key, _now, id)
                p.zadd(R_STAR_BY_USER_ID_CID%(user_id, cid), _now, id)
                p.zadd(R_STAR_BY_ID % id, time(), user_id)
                p.execute()

    @classmethod
    def rm(cls, user_id, id, cid):
        key = R_STAR_BY_USER_ID_CID % (user_id, 0)
        if redis.zrank(key, id) is not None:
            with redis.pipeline() as p:
                p.hincrby(R_STAR_COUNT, user_id, -1)
                p.hincrby(R_STAR_COUNT, id, -1)
                p.zrem(key, id)
                p.zrem(R_STAR_BY_USER_ID_CID%(user_id, cid), id)
                p.zrem(R_STAR_BY_ID % id, user_id)
                p.execute()

    @classmethod
    def count_by_id_list(cls, li):
        if li:
            return map(int, [i or 0 for i in redis.hmget(R_STAR_COUNT, *li)])
        return []

    @classmethod
    def user_id_list_by_id(cls, id):
        return map(int, redis.zrange(R_STAR_BY_ID % id, 0, -1, True))

    @classmethod
    def id_list_by_user_id(cls, user_id, cid=0):
        return map(int, redis.zrange(R_STAR_BY_USER_ID_CID % (user_id, cid) , 0, -1, True))

    @classmethod
    def count_by_id(cls, id):
        return int(redis.hget(R_STAR_BY_ID, id) or 0)
    
    @classmethod
    def is_star_by_id(cls, user_id, id, cid=0):
        key = R_STAR_BY_USER_ID_CID%(user_id, int(cid))
        return redis.zscore(key, id)

    @classmethod
    def is_star_by_id_list(cls, user_id, li, cid=0):
        if user_id:
            key = R_STAR_BY_USER_ID_CID%(user_id, int(cid))
            with redis.pipeline() as p:
                for i in li:
                    p.zscore(key, i)
                return p.execute()
        else:
            return [0]*len(li)

if __name__ == '__main__':
    print Star.is_star_by_id_list(2, [9931751], 20)
    print Star.is_star_by_id_list(2, [9931752, 23])


