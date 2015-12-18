#!/usr/bin/env python
#coding:utf-8
import _env
from __init__ import RpcView as _View
from z42.config import SSO
from json import loads
from time import time as _time
from tornado.web import HTTPError
from jsob import JsOb
from zapp._WEB.model.client_sign import ClientSign
from z42.config import DEBUG
# server 端 user_id app_id session 
# client 端 user_id


class ClientRpcView(_View):
    def prepare(self):

        time, sign = self.get_argument('s').split("|",2)

        time = int(time)

        server_time = _time()

        if not DEBUG:
            if abs(time - server_time) > 300: 
                raise HTTPError(401, "CLIENT TIME %s NOT MATCH RPC SERVER TIME %d"%(time, server_time)) 
        o = self.get_argument('o') 
        if not ClientSign.verify(sign, SSO.SECRET, o, time):
            raise HTTPError(401, "SIGN NOT MATCH")


