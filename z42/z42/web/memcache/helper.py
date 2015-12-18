#coding:utf-8
import os
from decorator import decorator
import inspect
from array import array
from struct import pack
#from __init__ import mc
from z42.web.memcache import mc

def _mc_get_dict(self, args_list, func=None):
    if not isinstance(args_list, (list, tuple, dict, set)):
        args_list = tuple(args_list)
    if args_list:
        result = self.get_list(args_list, func)
        return dict(zip(args_list, result))
    return {}

def _mc_decorator(self, key=None, expire=0):
    if type(key) is str:
        _key = key
        key = lambda x:_key.format(**x)
    elif key is None:
        key = lambda x:''

    def _func(func):
        arg_names, varargs, varkw, defaults = inspect.getargspec(func)

        if varargs or varkw:
            raise Exception('do not support varargs')

        defaults = defaults or {}
        if defaults:
            args = dict(zip(arg_names[-len(defaults):], defaults))
        else:
            args = {}


        def _(f, *a, **kw):
            aa = args.copy()
            aa.update(zip(arg_names, a))
            aa.update(kw)
            mc_key = key(aa)

            #print mc_key
            r = self.get(mc_key)
            if r is None:
                r = f(*a, **kw)
                self.set(mc_key, r, expire)
            return r

        return decorator(_, func)

    return _func

def _mc_delete(self, *args):
    key = self.key_pattern%args
    return mc.delete(key)

class McCacheM(object):
    def __init__(self, key_pattern):
        self.key_pattern = key_pattern

    def get(self, *args):
        key = self.key_pattern%args
        return mc.get_msgpack(key)

    def set(self, key, value, expire=0):
        return mc.set_msgpack(self.key_pattern%key, value, expire)

    def get_list(self, args_list, func=None):
        if func is not None:
            raise 'TODO'
        key_pattern = self.key_pattern
        key_list = [key_pattern%i for i in args_list]
        result = mc.get_list_msgpack(key_list)

        return result

    get_dict = _mc_get_dict
    __call__ = _mc_decorator
    delete = _mc_delete


class McCache(object):
    """

演示代码如下 ::

    mc_xxx = McCache("XXxxx:%s")

    @mc_xxx(lambda x:x['id'])
    def xxx(id):
        return id*3

    print  xxx("123")

    @mc_xxx("{id}")
    def xxx(id):
        return id*3

    print  xxx("467")
    print "MC GET"
    print mc_xxx.get("123")
    print mc_xxx.get_dict(["123","467"])
    mc_xxx.delete("123")


    """
    def __init__(self, key_pattern):
        self.key_pattern = key_pattern

    def get(self, *args):
        key = self.key_pattern%args
        return mc.get(key)

    def set(self, key, value, expire=0):
        return mc.set(self.key_pattern%key, value, expire)

    def get_list(self, args_list, func=None):
        key_pattern = self.key_pattern
        key_list = [key_pattern%i for i in args_list]
        result = mc.get_list(key_list)
        if func is not None:
            _result = result
            result = []
            for id, key, i in zip(args_list, key_list, _result):
                if i is None:
                    i = func(id)
                    if i is None:
                        i = 0
                    self.set(key, i)
                result.append(i)
        return result

    def decr(self, *args):
        key = self.key_pattern%args
        return mc.decr(key)

    def incr(self, *args):
        key = self.key_pattern%args
        return mc.incr(key)

    __call__ = _mc_decorator
    get_dict = _mc_get_dict
    delete = _mc_delete


class McCacheA(object):
    def __init__(self, key_pattern, type='L'):
        self.key_pattern = key_pattern
        self.type = type

    def get(self, *args):
        key = self.key_pattern%args
        result = mc.get(key)
        if result is not None:
            return array(self.type, result)

    def set(self, key, value, expire=0):
        key = self.key_pattern%key
        if type(value) is not array:
            value = pack(self.type*len(value), *value)
        else:
            value = value.tostring()
        return mc.set(key, value, expire)

    def get_list(self, args_list, func=None):
        if func is not None:
            raise  'TODO'
        if args_list:
            key_pattern = self.key_pattern
            key_list = [key_pattern%i for i in args_list]
            result = []
            for i in mc.get_list(key_list):
                if i is None:
                    result.append(i)
                else:
                    result.append(array(self.type).fromstring(i))
            return result
        else:
            return []

    __call__ = _mc_decorator
    get_dict = _mc_get_dict
    delete = _mc_delete


class McLimitA(object):
    McCls = McCacheA
    def __init__(self, key_pattern, limit):
        self.mc = self.McCls(key_pattern)
        self.limit = limit
        self.key_pattern = key_pattern

    def __call__(self, key, expire=0):
        if type(key) is str:
            _key = key
            key = lambda x:_key.format(**x)

        def _func(func):
            arg_names, varargs, varkw, defaults = inspect.getargspec(func)

            if varargs or varkw:
                raise Exception('do not support varargs')

            defaults = defaults or {}
            if defaults:
                args = dict(zip(arg_names[-len(defaults):], defaults))
            else:
                args = {}


            def _(f, *a, **kw):
                aa = args.copy()
                aa.update(zip(arg_names, a))
                aa.update(kw)
                mc_key = key(aa)
                offset = aa.get('offset', 0)
                limit = aa.get('limit')

                if limit is not None and offset+limit > self.limit:
                    return func(*a, **kw)

                smc = self.mc
                r = smc.get(mc_key)
                #print  mc_key,r
                if r is None:
                    aa['offset'] = 0
                    aa['limit'] = self.limit
                    r = f(**aa)
                    smc.set(mc_key, r, expire)

                if limit is None:
                    if self.limit > len(r):
                        return r[offset:]
                    return func(*a, **kw)

                return r[offset:limit+offset]

            return decorator(_, func)
        return _func


    def delete(self, *args):
        return self.mc.delete(*args)


class McLimit(McLimitA):
    McCls = McCache


class McLimitM(McLimitA):
    McCls = McCacheM


class McNum(object):
    def __init__(self, get_num, mc_key, timeout=36000):
        self.mc_key = mc_key
        self.get_num = get_num
        self.timeout = timeout


    def __call__(self, *key):
        mk = self.mc_key % '_'.join(map(str, key))
        num = mc.get(mk)
        if num is None:
            #print "self.get_num", key, self.get_num(*key)
            num = self.get_num(*key) or 0
            mc.set(mk, num, self.timeout)
        return num

    def get_dict(self, keys):
        mc_key = self.mc_key
        mc_key_list = dict([(key, mc_key%key) for key in keys])
        result = mc.get_dict(mc_key_list.itervalues())
        r = {}
        for k, mck in mc_key_list.iteritems():
            v = result.get(mck)
            if v is None:
                v = self.get_num(k) or 0
                mc.set(mck, v)
            r[k] = v
        return r

    def bind(self, xxx_list, property, key='id'):
        d = []
        e = []
        for i in xxx_list:
            k = getattr(i, key)
            if k:
                d.append(k)
                e.append((k, i))
            else:
                i.__dict__[property] = None

        r = self.get_dict(set(d))
        for k, v in e:
            v.__dict__[property] = r.get(k)

    def delete(self, *key):
        mk = self.mc_key % '_'.join(map(str, key))
        mc.delete(mk)

    def set(self, key, value):
        mk = self.mc_key % key
        mc.set(mk, value)

    def get_list(self, keys):
        r = self.get_dict(keys)

        return [
            r.get(i, 0) for i in keys
        ]

    def incr(self, *key):
        mk = self.mc_key % '_'.join(map(str, key))
        if mc.get(mk) is not None:
            mc.incr(mk)

    def decr(self, *key):
        mk = self.mc_key % '_'.join(map(str, key))
        if mc.get(mk) is not None:
            mc.decr(mk)




#def mc_func_get_dict_with_key_pattern(mc, func, key_list, key_pattern):
#    t = mc.get_dict(key_pattern % i for i in key_list)
#    result = {}
#    for i in key_list:
#        key = key_pattern % i
#        o = t[key]
#        if o is None:
#            o = func(*i)
#        result[i] = o
#    return result
#
#
#
#
#def mc_func_get_dict(mc, func, key_list):
#    t = mc.get_dict(key_list)
#    for i in key_list:
#        if t[i] is None:
#            t[i] = func(i)
#    return t
