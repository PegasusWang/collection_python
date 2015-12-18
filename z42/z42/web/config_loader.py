#coding:utf-8
import _env
from jsob import JsOb
from _import import _import
from os.path import dirname
import sys
from os.path import exists, join
import logging
import traceback

CONFIG_LOADED = []

def _load(local, *args):
    self = JsOb()

    prepare_list = [ ]
    finish_list = [ ]
    dirpath = dirname(local['__file__'])
    sys.path.insert(0, dirpath)
    global CONFIG_LOADED

    def _load(name):
        if not exists(join(dirpath, '%s.py'%name.replace('.', '/'))):
            return
        try:
            mod = _import(name)
        except ImportError:
            logging.warning('ImportError %s'%name)
            import traceback
            logging.warning(traceback.format_exc())
            return

        if mod is None:
            return

        if mod in CONFIG_LOADED:
            CONFIG_LOADED.pop(CONFIG_LOADED.index(mod))
        CONFIG_LOADED.append(mod)

        mod.__file__.rsplit('.', 1)[0]

        prepare = getattr(mod, 'prepare', None)
        if prepare:
            prepare_list.append(prepare)

        finish = getattr(mod, 'finish', None)
        if finish:
            finish_list.append(finish)

    for i in args:
        _load(i)

    funclist = prepare_list+list(reversed(finish_list))
    for _ in funclist:
        _(self)
    local.update(self.__dict__)
    sys.path.pop(0)
    return self



__ARGS = [
    'default',
]
try:
    import socket
except ImportError:
    pass
else:
    __ARGS.append(
        '_host.%s' % socket.gethostname(),
    )
import logging
import os
#/base/data/home/apps/s~btcv02/251.373207131573752161/z42/config/__init__.pyc GAE
if 'APPENGINE_RUNTIME' in os.environ:
    DEV_SERVER = os.environ['SERVER_SOFTWARE'].startswith('Development')
    if DEV_SERVER:
        __user = __file__[__file__.find('/home/'):].split('/')[2]
        __ARGS.append(
            '_user.%s' % __user ,
        )
else:
    try:
        import getpass
        import pwd
        __user = getpass.getuser()
    except (ImportError, AttributeError):
        pass
    else:
        __ARGS.append(
            '_user.%s' % __user ,
        )


def load(local):
    logging.info('LOADING CONFIG %s'%__ARGS)
    _load(
        local, *__ARGS
    )






