#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tornado import web, ioloop, gen
from random import random


n = 1
class Main(web.RequestHandler):
    def get(self):
        global n
        n+=1
        print(n)
        self.write('hehe'*10)


class Sleep(web.RequestHandler):
    @gen.coroutine
    def get(self):
        yield gen.sleep(random())
        self.write('hehe'*1000)


app = web.Application(
    [
        (r'/', Main),
        (r'/test', Sleep)
    ],
    debug=True
)


if __name__ == '__main__':
    app.listen(8000)
    try:
        ioloop.IOLoop.current().start()
    except:
        ioloop.IOLoop.current().stop()
