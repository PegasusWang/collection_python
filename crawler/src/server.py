#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tornado import web, ioloop, gen


n = 1
class Main(web.RequestHandler):
    def get(self):
        global n
        n+=1
        print(n)
        self.write('hehe'*10)


app = web.Application(
    [(r'/', Main)],
    debug=True
)


if __name__ == '__main__':
    app.listen(8080)
    try:
        ioloop.IOLoop.current().start()
    except:
        ioloop.IOLoop.current().stop()
