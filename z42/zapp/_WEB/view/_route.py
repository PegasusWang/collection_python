#!/usr/bin/env python
#coding:utf-8

import _env
from zapp._WEB.model.host import cid_by_host
from z42.web.route import Route

class _CidMatch(object):
    pattern = None
    def __init__(self, cid):
        self.cid = cid

    def match(self, host):
        if cid_by_host(host) == self.cid:
            return True

class RouteByCid(Route):
    def __init__(self, cid, prefix=''):
        self.handlers = []
        self._prefix = prefix
        self.host = _CidMatch(cid)


