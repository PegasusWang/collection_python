#!/usr/bin/env python
# coding:utf-8
import _env
import tornado.locale
from os.path import join
import logging
from jsob import JsOb
import tornado.escape
import re
import yajl
tornado.escape.json=  yajl

try:
    from z42.config import APP
except ImportError:
    print 'APP not set'
else:
    #tornado.locale.load_gettext_translations(
    #    join(_env.PREFIX, "i18n"), APP
    #)
    tornado.locale.set_default_locale('en_US')
try:
    from tornado import httpserver
    _init = httpserver.HTTPRequest.__init__

    def __init__(self, *args, **kwds):
        _init(self, *args, **kwds)
        if self.method == 'POST':
            if 'Content-Type' not in self.headers:
                self.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    httpserver.HTTPRequest.__init__ = __init__
except ImportError:
    pass


from tornado import web

def _execute_method(self):
    if not self._finished:
        args = self.path_args
        kwargs = self.path_kwargs
        if hasattr(self, 'init'):
            getattr(self, 'init')(*args, **kwargs)
            if self._finished:
                return
        method = getattr(self, self.request.method.lower())
        self._when_complete(method(*args, **kwargs), self._execute_finish)

web.RequestHandler._execute_method = _execute_method

def decode_argument(self, value, name=None):
    return value

web.RequestHandler.decode_argument = decode_argument 

from tornado.web import URLSpec
def add_handlers(self, host_pattern, host_handlers):
    """Appends the given handlers to our handler list.

    Host patterns are processed sequentially in the order they were
    added. All matching patterns will be considered.
    """
    handlers = []
    # The handlers with the wildcard host_pattern are a special
    # case - they're added in the constructor but should have lower
    # precedence than the more-precise handlers added later.
    # If a wildcard handler group exists, it should always be last
    # in the list, so insert new groups just before it.
    if isinstance(host_pattern, basestring):
        if not host_pattern.endswith('$'):
            host_pattern += '$'
        if self.handlers and self.handlers[-1][0].pattern == '.*$':
            self.handlers.insert(-1, (re.compile(host_pattern), handlers))
        else:
            self.handlers.append((re.compile(host_pattern), handlers))
    else:
        self.handlers.append((host_pattern, handlers))

    for spec in host_handlers:
        if isinstance(spec, (tuple, list)):
            assert len(spec) in (2, 3, 4)
            spec = URLSpec(*spec)
        handlers.append(spec)
        if spec.name:
            if spec.name in self.named_handlers:
                app_log.warning(
                    'Multiple handlers named %s; replacing previous value',
                    spec.name)
            self.named_handlers[spec.name] = spec

import tornado.web
tornado.web.Application.add_handlers = add_handlers
