#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tornado import web, ioloop, gen


class Main(web.RequestHandler):
    def get(self):
        self.write('hehe'*100)


app = web.Application(
    [(r'/', Main)],
    debug=True
)


if __name__ == '__main__':
    app.listen(8000)
    try:
        ioloop.IOLoop.current().start()
    except:
        ioloop.IOLoop.current().stop()
