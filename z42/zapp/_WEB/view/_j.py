#!/usr/bin/env python
#coding:utf-8

import _env
import json
import tornado
from yajl import loads, dumps
from zapp._WEB.view._user import View


class JsonLoginView(View):

    def prepare(self):
        super(JsonLoginView, self).prepare()
        if not self.current_user_id:
            callback = self.get_argument('callback', None)
            result = '{"err":{"code": 403}}'
            if callback:
                result = "%s(%s)"%(callback,result)
            self.finish(result)

