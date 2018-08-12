#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random

import tornado
from tornado.web import RequestHandler


class SleepHandler(RequestHandler):

    @tornado.gen.coroutine
    def get(self, name):
        yield tornado.gen.sleep(1)
        return name


app = tornado.web.Application(
    [
        (r'/(.*)', SleepHandler)
    ], debug=True
)


app.listen(5000)
try:
    tornado.ioloop.IOLoop.current().start()
except:
    tornado.ioloop.IOLoop.current().stop()
