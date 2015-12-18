#!/usr/bin/env python
#coding:utf-8
import _env
import _patch
import logging
import sys
import tornado.wsgi
import wsgiref.handlers
from z42.config import DEBUG


def application(
    route_list,
    Application,
    xsrf_cookies=False,
):
    app = Application(
        xsrf_cookies=xsrf_cookies,
        debug=DEBUG,
        gzip=True
    )

    for route in route_list:
        app.add_handlers(route.host , route.handlers)

    return app
