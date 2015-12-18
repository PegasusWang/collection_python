# coding:utf-8

import _env
from z42.config import APP
from zapp._WEB.view._user import View as _View
import css
import js
from z42.web.render import render
from zapp._WEB.model.ob import Ob



class View(_View):
#    @property
#    def xsrf_form_html(self):
#        return '<input type="hidden" name="_xsrf" value="%s">' % self.xsrf_token
#
#    @property
#    def _xsrf(self):
#        return '_xsrf=%s' % self.xsrf_token

    def render(self, template_name=None, **kwds):
        if not self._finished:
            if template_name is None:
                if not hasattr(self, 'template'):
                    path = self.__module__.split('.')
                    path.pop(0)
                    path.pop(1)  # 原来的第3个
                    self.template = '/%s/%s.html' % (
                        '/'.join(path),
                        self.__class__.__name__
                    )
                template_name = self.template
            current_user = self.current_user
            kwds['request'] = self.request
            kwds['this'] = self
            kwds['css'] = css
            kwds['js'] = js
#            kwds['_xsrf'] = self._xsrf
            kwds['current_user'] = self.current_user
            kwds['current_user_id'] = self.current_user_id
            #           kwds['_T'] = _T
            self.finish(render(template_name, **kwds))

class NoLoginView(View):
    def prepare(self):
        super(NoLoginView, self).prepare()
        if self.current_user_id:
            return self.redirect("/")


class LoginView(View):
    _login_template_name = "/%s/sso/index.html"%APP

    def prepare(self):
        super(LoginView, self).prepare()
        if not self._finished:
            user_id = self.current_user_id
            if not self.current_user_id:
                self.render(self._login_template_name, action="login")


