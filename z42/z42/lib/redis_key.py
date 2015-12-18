#coding:utf-8
from intstr import IntStr

#print len('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz')

redis_keyer = IntStr(
'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'
)

REDIS_KEY_ID = 'RedisKeyId'
REDIS_KEY = 'RedisKey'
REDIS_ID_KEY = 'RedisIdKey'

_EXIST = set()

class RedisKey(object):
    def __init__(self, redis):
        self.redis = redis

    def __getattr__(self, attr):
        def _(name=''):
            return self(attr, name)
        return _

    def __call__(self, attr, name=''):
        key = attr+name
        redis = self.redis
        if key in _EXIST:
            raise Exception('redis key is already defined %s'%key)
        _EXIST.add(key)
        if redis:
            _key = redis.hget(REDIS_KEY, key)
            if _key is None:
                id = redis.incr(REDIS_KEY_ID)
                _key = redis_keyer.encode(id)
                if name and '%' in name:
                    _key = _key+"'"+name
                p = redis.pipeline()
                p.hset(REDIS_KEY, key, _key)
                p.hset(REDIS_ID_KEY, _key, key)
                p.execute()
            return _key




if __name__ == '__main__':
    pass
    for i in redis.hgetall("RedisIdKey"):
        print i
