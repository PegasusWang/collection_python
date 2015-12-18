import os
import marshal as msgpack

class SimpleCached:
    ' cache obj in local process, wrapper for memcache '
    def __init__(self, mc):
        self.mc = mc

    def set_msgpack(self, key, val, time=0, dumps=msgpack.dumps):
        val = dumps(val)
        self.mc.set(key, val, time)

    def get_msgpack(self, key, loads=msgpack.loads):
        r = self.mc.get(key)
        if r is not None:
            r = loads(r)
        return r

    def get_dict_msgpack(self, keys, loads=msgpack.dumps):
        rs = self.mc.get_multi(keys)
        rs = dict((k, loads(v)) for k, v in rs.iteritems())
        return rs

    def get_dict(self, keys):
        return self.mc.get_multi(keys)

    def get_list_msgpack(self, keys, loads=msgpack.loads):
        rs = self.get_dict_msgpack(keys, loads)
        return [rs.get(k) for k in keys]

    def __getattr__(self, name):
        def func(*args, **kwargs):
            return getattr(self.mc, name)(*args, **kwargs)
        return func

    def reset(self):
        pass

class LocalCached:
    ' cache obj in local process, wrapper for memcache '

    def __init__(self, mc):
        self.mc = mc
        self.reset()

    def reset(self):
        self.dataset = {}
        self.dataset_msgpack = {}

    def start_log(self):
        mc = self.mc
        if not hasattr(mc, 'obj'):
            self.mc = self.logger(mc)

    def stop_log(self):
        mc = self.mc
        if hasattr(mc, 'obj'):
            self.mc = mc.obj

    def get_log(self):
        from collections import defaultdict
        d = defaultdict(int)
        nd = defaultdict(lambda: [0, 0])
        for call, ncall, cost in self.mc.log:
            d[call] += 1
            x = nd[ncall]
            x[0] += 1
            x[1] += cost
        result = 'memcache access (%s/%s calls):\n\n%s\nDetail:\n\n%s\n' % \
                        (len(d), sum(d.itervalues()),
                         ''.join('%s: %d times, %f seconds\n' % (
                                                ncall, times, cost)
                                 for ncall, (times, cost)
                                 in sorted(nd.iteritems())),
                         ''.join('%s: %d times\n' % (key, n)
                                 for key, n in sorted(d.iteritems())))
        result = result.replace('get_multi', 'get_dict')
        return result

    def __repr__(self):
        return 'Locally Cached ' + str(self.mc)

    def set(self, key, val, time=0):
        self.dataset[key] = val
        self.mc.set(key, val, time)

    def set_msgpack(self, key, val, time=0, dumps=msgpack.dumps):
        self.dataset_msgpack[key] = val
        val = dumps(val)
        self.mc.set(key, val, time)

    def get(self, key):
        r = self.dataset.get(key)
        if r is None:
            r = self.mc.get(key)
            if r is not None:
                self.dataset[key] = r
        return r

    def get_msgpack(self, key, loads=msgpack.loads):
        r = self.dataset_msgpack.get(key)
        if r is None:
            r = self.get(key)
            if r is not None:
                r = loads(r)
                self.dataset_msgpack[key] = r
        return r

    def get_dict(self, keys):
        if keys:
            rs = [(k, self.dataset.get(k)) for k in keys]
            r = dict((k, v) for k, v in rs if v is not None)
            rs = self.mc.get_multi([k for k, v in rs if v is None])
            r.update(rs)
            self.dataset.update(rs)
            return r
        else:
            return {}

    def get_dict_msgpack(self, keys, loads=msgpack.loads):
        rs = [(k, self.dataset_msgpack.get(k)) for k in map(str,keys)]
        r = dict((k, v) for k, v in rs if v is not None)
        rs = self.mc.get_multi([k for k, v in rs if v is None])
        rs = dict((k, loads(v)) for k, v in rs.iteritems())
        r.update(rs)
        self.dataset_msgpack.update(rs)
        return r

    def get_list_msgpack(self, keys, loads=msgpack.loads):
        rs = self.get_dict_msgpack(keys, loads)
        return [rs.get(k) for k in keys]

    def get_list(self, keys):
        if keys:
            rs = self.get_dict(keys)
            return [rs.get(k) for k in keys]
        else:
            return []
    def append(self, key, val):
        self.dataset.pop(key, None)
        return self.mc.append(key, val)

    def prepend(self, key, val):
        self.dataset.pop(key, None)
        return self.mc.prepend(key, val)

    def delete(self, key):
        self.dataset.pop(key, None)
        return self.mc.delete(key)

    def decr(self, key, val=1):
        self.dataset.pop(key, None)
        return self.mc.decr(key, val)

    def incr(self, key, val=1):
        self.dataset.pop(key, None)
        return self.mc.incr(key, val)

    def __getattr__(self, name):
        def func(*args, **kwargs):
            return getattr(self.mc, name)(*args, **kwargs)
        return func



def init_mc(mc, disable_local_cached=False):

    if disable_local_cached:
        mc = SimpleCached(mc)
    else:
        mc = LocalCached(mc)
    return mc


