

.. _views: 

==================================================
视图介绍
==================================================

:作者: 王然 kxxoling@gmail.com



View
-------------------------------------

HostView
-------------------------------------

页面视图通常继承自该类，示例代码::

    from zapp.SITE.misc.web.host_view import HostView
    @route('/')
    class index(HostView):
        def get(self):
            self.render()


JsonErrView
-------------------------------------

该 class 提供一个返回 JSON 文件的 render() 方法，通常用于 Ajax 后台验证。示例代码::

    from z42.web.view.j import JsonErrView
    from zapp.SITE.misc.web.host_view import HostView

    @route('/j/m')
    class _(JsonErrView, HostView):
        def post(self):
            err = JsOb()
            # 为 err 添加内容
            self.render(err)


LoginView
-------------------------------------

该 class 提供登录验证，需要登录的视图继承该视图。示例代码::
    
    from zapp.SITE.view._base import LoginView
    from zapp.SITE.misc.web.host_view import HostView
    @route('/user/manage')
    class _(LoginView, HostView):
        def get(self):
            self.render()


LoginHostView
--------------------------------------

JsonLoginView
--------------------------------------

HostAdminView
--------------------------------------

JsonHostAdminView
--------------------------------------


