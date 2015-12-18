#!/usr/bin/env python
#coding:utf-8
import _env
from os import urandom
from tornado.web import HTTPError
from zapp._WEB.view._user import View as _View
from yajl import dumps
from json import loads
from jsob import JsOb

class Err(JsOb):
    pass

def logined(func):
    def _(self, *args, **kwds):
        if self.current_user_id:
            return func(self, *args, **kwds)
        err = Err()
        err.code = 403
        return err
         
    return _

    
class RpcView(_View):
    DISABLED = set([i for i in dir(_View) if not i.startswith("_")])


    def redirect(self, url):
        callback = self.get_argument('callback',0)
        if callback:
            url+="&callback=%s"%callback
        super(RpcView,self).redirect(url)

    def _call(self, func_name, o): 
        if func_name.startswith("_") or func_name in self.DISABLED:
            raise HTTPError(400)

        func = getattr(self,func_name, None)
        if func is None:
            raise HTTPError(501)

        if o is not None:

            o = loads(o)
            type_o = type(o)

            if type_o is list:
                r = func(*o)
            elif type_o is dict:
                r = func(**o) 
            else:
                r = func(o)
        else:
            r = func()
        if r is None:
            chunk = '{}'
        elif isinstance(r, Err) and r: 
            chunk = '{"err":%s}'%str(r)
        elif isinstance(r, JsOb): 
            chunk = str(r)
        else:
            chunk = dumps(r)
        return chunk

    def get(self, func_name):
        chunk = self._call(func_name, self.get_argument('o', None))
        if not self._finished:
            callback = self.get_argument('callback', 0)
            if callback:
                chunk = "%s(%s)"%(callback, chunk)

            self.finish(chunk) 

    def post(self, func_name):
        chunk = self._call(func_name, self.request.body or None)
        if not self._finished:
            self.finish(chunk)

def rpc_url(url):
    return url+"\\.(.*)"


#　o=[time, user_id, {info_id ,  session} ]&s=3242342432zvsdzg
#  secret+o = sha512 == sign
# prepare
# 超过５
# self.current_user_id = user_id
# self.json = JsOb()

# presync

# o=[time,user_id, {'key':['name','ico', 'ico_crop', 'mail']}]&s=xcvwgaweg232

# sync

class LoginedRpcView(RpcView):
    def prepare(self):
        super(LoginedRpcView,self).prepare()
        if not self.current_user_id:
            self.finish('{"err":{"code":403}}')
