.. _hg_tutorial: 

==================================================
Hyper Estraier 简明教程
==================================================

:作者: tonghs tonghuashuai@gmail.com

About 
----------------------
Hyper Estraier is a full-text search system. You can search lots of documents for some documents including specified words. If you run a web site, it is useful as your own search engine for pages in your site. Also, it is useful as search utilities of mail boxes and file servers. 

http://fallabs.com/hyperestraier/

目前 天使汇 网站的全文搜索部分使用 Hyper Estraier 实现。

Install
----------------------
::

    emerge hyperestraier

Configuration
----------------------
1. 建立工作目录::

    mkdir /mnt/data1/42web

#. 设置路径读写权限
#. 在工作目录下执行::
   
    estmaster init .

#. 删除工作目录下的配置文件，并执行:: 
   
    ln -s ~/42web/zapp/SITE/misc/config/hyperestraier/_conf .

#. 启动 hyperestraier:: 

    estmaster start .

#. 启动服务::
   
   zapp/SITE/model/rpc/server/run.py
   zapp/SITE/model/rpc/server/search.py

#. 访问 http://域名:1978，进入 web 管理页面（默认用户名密码 admin admin）

#. 建立索引数据库 ob0 ob10000 ob20000

   单击 Manage Nodes，在出现的页面填写 node 信息，第一个文本框为 name，第二个文本框为 label。

Other
----------------------
* 用户管理

Select Manage Users. There are input boxes for user name, password, flags, full name and miscellaneous information at bottom. Enter following data for new user: "clint", "tnilc", "s", "Clint Eastwood" and "Dirty Harry". Flag "s" denotes user with super user privileges. User name is limited to alphanumeric characters only.

详细见：http://fallabs.com/hyperestraier/nguide-en.html 中的 Administration Interface 章节
