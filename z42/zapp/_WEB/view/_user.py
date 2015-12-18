#!/usr/bin/env python
#coding:utf-8

import _env
from z42.web.view import View as _View
from jsob import JsOb
from zapp._WEB.model.session import Session
from zapp._WEB.model.ob import Ob
from z42.config import HOST

class UserDict(JsOb):
    def __nonzero__(self):
        return 0

class View(_View):
    _USER_COOKIE_NAME = "S"
    def get_current_user(self):
        current_user_id = self.current_user_id
        if current_user_id:
            user =  Ob.find_one(dict(id=current_user_id))
            if user is not None:
                return user
            else:
#                print self._USER_COOKIE_NAME, "!!"
                self.clear_cookie(self._USER_COOKIE_NAME, domain="."+HOST )
                self.current_user_id = 0
        o = UserDict()
        #o.id = 0
        #o.name = ''
        #o.ico = 0
        return o

    @property
    def current_user_id(self):
        if not hasattr(self, '_current_user_id'):
            s = self.get_cookie(self._USER_COOKIE_NAME)
            self._current_user_id = 0

            if s:
                user_id = Session.decode(s)
                if user_id: 
                    self._current_user_id = user_id 

            if not self._current_user_id:
                if s:
                    host = self.request.host
                    self.clear_cookie(self._USER_COOKIE_NAME, domain="."+HOST )

        return self._current_user_id

    @current_user_id.setter
    def current_user_id(self, value):
        self._current_user_id = value


if __name__ == '__main__':
    import sys
    if sys.getdefaultencoding() == 'ascii':
        reload(sys)
        sys.setdefaultencoding('utf-8')





