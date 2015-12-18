#coding:utf-8
#try:
#    import astoptimizer
#except ImportError:
#    pass
#else:
#    astoptimizer.patch_compile(
#        astoptimizer.Config('builtin_funcs', 'pythonbin')
#    )

import sys
from os.path import dirname, abspath, exists, join

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


PREFIX = dirname(abspath(__file__))
def _():
    global PREFIX
    PWD = abspath(__file__)
    while True and len(PWD) > 1:
        PWD = dirname(PWD)
        if exists(join(PWD, 'z42/web/boot')):
            PREFIX = PWD

    for path in (
#        join(PREFIX, 'z42/virtualenv.zip'),
        join(PREFIX, 'z42/lib'),
        PREFIX,
    ):
        if path :
            if path in sys.path:
                sys.path.remove(path)
            sys.path.insert(0, path)


#    import yajl
#    import json
#
#    json.dump = yajl.dump
#    json.dumps = yajl.dumps
#    json.loads = yajl.loads
#    json.load = yajl.load

#    print PREFIX,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#    print PREFIX in sys.path
#    print sys.path

#    from json import dumps, loads
#    import json
#    _json_dumps = dumps
#    _json_loads = loads
#    try:
#        from ujson import dumps, loads
#    except ImportError:
#        pass
#
#
#    def _dumps(*args, **kwds):
#        if 'ensure_ascii' not in kwds:
#            kwds['ensure_ascii'] = False
#        if 'parse_float' in kwds:
#            return _json_dumps(*args, **kwds)
#        return dumps(*args, **kwds)
#    def _loads(*args, **kwds):
#        if 'parse_float' in kwds:
#            return _json_loads(*args, **kwds)
#        return loads(*args, **kwds)
#
#    json.dumps = _dumps
#    json.loads = _loads

    import z42._app_config_
    import z42.config._signal

_()
