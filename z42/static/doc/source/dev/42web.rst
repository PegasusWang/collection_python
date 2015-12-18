42WEB 框架使用不完全手册
=====================================================================


如何写文档
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

开发服务器上，文档的默认路径是 ::

    ~/42web/static/doc/source

写完之后，在 ::

    ~/42web/static/doc/

运行 ::

    make html

可以生成html， 访问 http://doc.你的域名, 可以浏览你新生成的文档


编码规范
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

我们python编码风格参见 `Python 编码风格指南 <http://code.google.com/p/zhong-wiki/wiki/PEP8>`_

一般而言，我们尽量使用英文单词的完整写法，而不使用缩写，以免陷入每个人缩写不统一的混乱局面。

html / css / coffee / model 命名（函数名，文件名）保持一致，这样找到了其中一个，就能方便地定位其他的所有。

html 的编码规范 我们参考 `Google HTML/CSS代码风格指南 <http://chajn.org/htmlcssguide/htmlcssguide.html>`_

简单的说， 单元素标记（比如input，br，img，link，meta，hr等等）不要闭合。


不要view中直接调用redis，mongo去操作数据库，通过model层将其封装为接口再调用


redis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


首先请阅读

* `REDIS 中文文档 <http://www.redisdoc.com/en/latest/>`_


使用演示 zapp/SITE/model/password_reset.py ::

    import _env
    from b64uuid import b64uuid
    from z42.config import HOST
    from zapp.SITE.model._db import redis, R

    EXPIRE = 7*3600*24

    R_PASSWORD_RESET = R.PASSWORD_RESET('%s')

    def password_reset_link(user_id):
        key = R_PASSWORD_RESET%user_id
        token = redis.get(key)
        if not token:
            token = b64uuid()
            redis.setex(key, EXPIRE, token)

        return 'http://auth.%s/password_reset_verify/%s_%s'%(HOST, user_id, token)

    def password_reset_verify(user_id, token):
        return token and (token == redis.get(R_PASSWORD_RESET%user_id))

用法说明 

因为redis的内存数据库，所以我们通过 R 来生成 redis 的 key 以节省内存占用 , R的用法如 ::
        
        R_AAA = R.AAA()
        R_BBB = R.BBB('%s')

扩展阅读 `节约内存：Instagram的Redis实践 <http://blog.nosqlfan.com/html/3379.html>`_



开发流程
---------------

新建一个页面通常需要创建几个文件：

* 模板 zapp/SITE/model/模块名.py
* 视图 zapp/SITE/view/模块名.py
* Coffee Script 脚本 coffee/SITE/auth/模块名/视图名.coffee 
* Make 模板 html/SITE/auth/模块名/视图名.html
* CSS 样式文件 css/SITE/auth/模块名.css

并在 `_url.py` 中注册视图。


Mako 模板
---------------

Mako 模板的存放路径通常是 42web/html/SITE/模块名/文件名.html。 
Mako 模板的使用见 `教程 <http://docs.makotemplates.org/en/latest/>`_ ，通用部分通常需要剥离成一个 _base.html 文件中，
不被直接 render 的模板命名以下划线 `_` 开头。

一个基本的模板文件大概是这样的::

    ## 这里继承父模版
    <%inherit file="/SITE/_base/default.html" />
    ## 添加头文件、CSS 文件
    <%block name="head">
    ## 这里引入 CSS 文件，将目录名中的斜线换成下划线作为变量传入
    <link rel="stylesheet" href="${css.SITE_auth_m}">
    </%block>
    
    <%block name="script">
    ## 在文件尾引入 JS 文件，变量名同为替换后的目录名，JS 文件来自于编译 Coffee Script
    <script src="${js.SITE_auth_m_m}"></script>
    </%block>


几个注意点：

1. 每个html模板都应该继承对应的基模板，不要直接写html

#. js如果不写在block中会造成无法加载的问题


Coffee Script
----------------

网页脚本用 Coffee Script，写完后需编译为 JavaScript
（添加新的 CS 脚本需要手动重启 dev.sh 脚本，修改已存在的脚本会自动编译成 JS）。


Python Model
-----------------

数据存储使用的是 MongoDB，通过封装过的 MongoKit 将数据 model 对应上 MongoDB 文档，
需要 `from z42.web.mongo import mongo` 。下面是一个简单的 model 文件示例::

    from z42.web.mongo import Doc 
    from z42.web.mongo import mongo 

    class UserIM(Doc):
        structure = {
            'user_id': int,
            'phone': basestring,
            'qq': basestring,
            'weixin':basestring
        }

创建一个 UserIM 对象使用 upsert() 方法，如 `UserIM({'phone': PHONE}).upsert({user_id: 1001})` ，
这行代码的作用是：如果存在 user_id 为 1001 的 UserIM，则将其 'phone' 设置为 PHONE，
否则在 MongoDB 中插入这样一个 JSON 文档： {'user_id': 1001, 'phone': PHONE}。


Python View
-----------------

web 开发使用的框架是修改过的 Tornado，需要通过装饰器注册 URL。
新建一个简单的 view 如下::

    from _route import route
    from z42.web.view.j import JsonErrView
    from jsob import JsOb
    from zapp.SITE.view._base import HostView
    
    @route('/m/register/')
    class register(HostView):
        def get(self, sign):
            self.render()

    @route('/j/m/')
    class _(JsonErrView, HostView):
        def post(self, sign):
            err = JsOb()            # 使用 JsOb 对象保存错误信息
            o = self.json           # 获取 JSON 化的 POST 信息
            if not o.title:
                err.title = "链接已失效！"
            if not err:
                do_something()
            self.render(err)

这个 module 注册了两个 view，一个注册页面和一个 Ajax 接口。route 方法是一个用于注册 URL 的装饰器，
装饰在 Handler class（通常继承自XxxView）上即可。

register class 就是视图 Handler 的最简写法。对于 Ajax 视图，Handler 名意义不大，可以使用下划线命名。
需要返回错误提示的视图，可以继承 JsonErrView。View 的继承用法详见 :ref:`views` 

扩展阅读
-----------------

`MongoDB权威指南 <https://code.google.com/p/mycloub/downloads/detail?name=%5B%E4%B8%AD%E6%96%87%E7%89%88%5D%20MongoDB%E6%9D%83%E5%A8%81%E6%8C%87%E5%8D%97.pdf>`_
 
