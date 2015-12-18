#!/usr/bin/env python
# coding:utf-8
import _env

import redis as _redis
#print _redis.__file__
from z42.config import REDIS_CONFIG
from redis_key import RedisKey

redis = _redis.StrictRedis(**REDIS_CONFIG)

R = RedisKey(redis)

from z42.web.mongo import Doc

if __name__ == '__main__':
    print REDIS_CONFIG
    print redis.get(R.ICO_URL("%s")%100000011)
    from pprint import pprint    
    print pprint(redis.info())
