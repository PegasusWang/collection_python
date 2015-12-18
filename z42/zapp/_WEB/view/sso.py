#!/usr/bin/env python
# coding:utf-8
import _env
from zapp._WEB.view._base import View,  NoLoginView
from zapp._WEB.model.sso_sign import sso_sign
from zapp._WEB.view._j import JsonLoginView 
from zapp._WEB.model.id_by_sso import id_by_sso_id, sso_id_by_id
from zapp._WEB.model.session import Session 
from _route import route
from jsob import JsOb
from json import dumps
from z42.config import HOST


@route('/sso/(login|new)')
class index(NoLoginView):
    def get(self, action):
        return self.render(action=action)


@route('/sso/(password_reset|mail_verify)/(.+)')
class mail_verify(NoLoginView):
    def get(self, action, code):
        self.render(action=action, code=code)

# @route('/sso/logout/(\d+)')
# class index(View):
#     def get(self, user_id):
#         user_id = int(user_id)
#         if self.current_user_id == user_id:
#             self.clear_cookie('S', domain="."+HOST)
#         self.redirect("/")

