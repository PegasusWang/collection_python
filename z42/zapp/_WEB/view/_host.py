#!/usr/bin/env python
#coding:utf-8
import _env
from zapp._WEB.view._base import View 
from zapp._WEB.model.host import host_id_by_host

class HostView(View):

    def prepare(self):
        super(HostView, self).prepare()
        self.host_id = host_id_by_host(self.request.host)
        self.host = Ob.find_one(dict(id=self.host_id))

class HostAdminView(LoginView, HostView):
    _405_template_name = "/%s/_base/405.html"%APP

    def prepare(self):
        super(HostAdminView, self).prepare()
        if not self._finished:
            if not self.host.can_admin(self.current_user_id):
                self.render(self._405_template_name)

class JsonHostLoginView(JsonLoginView, HostView):
    def prepare(self):
        super(JsonHostLoginView, self).prepare()

class JsonHostAdminView(JsonHostLoginView):
    def prepare(self):
        super(JsonHostAdminView, self).prepare()
        if not self._finished:
            if not self.host.can_admin(self.current_user_id):
                self.render({"code": 405})
