# coding:utf-8
import _env
import sys
from z42.web import cgi
import tornado.web
def main(route, port):
    if len(sys.argv) != 1 and sys.argv[1][:6] == '--port':
        port = sys.argv[1].rsplit('=')[1]


    print 'SERVE ON PORT %s'%port
#    print route.handlers
    application = cgi.application(route, tornado.web.Application)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


#import os
#print sys.path
#from os.path import abspath, join, dirname
#from view._route import route

if __name__ == '__main__':
    from z42.config import APP, HOST, PORT_BEGIN
    from importlib import import_module
    print HOST
    __import__('zapp.%s.view._url'%APP)
    ROUTE_LIST = import_module('zapp.%s.view._route'%APP).ROUTE_LIST
    main(reversed(ROUTE_LIST), PORT_BEGIN)
