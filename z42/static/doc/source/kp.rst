程序员知识点考评大纲
===================================



常用工具
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Linux 
----------------------------------

基础篇
..................................
* locate
* ag
* xtail

Gentoo
----------------------------------
* emerge --autounmask-write 然后 etc-update 然后 -3
* emerge =xxx-版本号

自定义的命令
..................................
* dirreplace
* replace_line.py
* deltmp

高级篇
..................................
* dstat
* dirreplace
* replace_line.py


tmux
-----------------------------------
* Ctrl+B

xshell
-----------------------------------

vim
-----------------------------------
* F12
* MR
* 批量注释
* = 排版
* vsp
* 替换
* 替换选中部分

版本控制
-----------------------------------

* hg

  - blame
  - log
    + -l 
  - fetch 
  - st
  - ignore
  - diff
  - grep 
  - bisect 定位BUG出现的版本 
  - serve
  - resolve
    + -l
    + -m

42web小工具 :

    ./hg_close_branch  
    ./hg_update_branch


前端
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HTML
-----------------------------------
* label for属性

  绑定表单元素id，实现点击label选中相应radio或checkbox
* 链接都必须写上href属性， 空链接请写成:: 

    <a href="javascript:void(0)"></a>

* 反复出现的按钮图标用 a标签 配合 css设置背景图 来实现，不要反复的写img标签（减少代码的冗余度）

CSS
-----------------------------------
* 模块分级
    * 全局级
    * 模块级
    * 页面级
* 分栏布局

  例如左宽665px,父容器宽1000px,在layout.css中定义::

  .R665{float: left; margin-left: 688px; width:312px;}
  .L665{float: left; width: 665px; margin-left: -100%;}

  参考:

  `双飞翼布局 <http://www.dqqd.me/flying-wing/>`_
  `常见布局 <http://blog.html.it/layoutgala/>`_

* 绝对底部

  `CSS Sticky Footer <http://paranimage.com/css-sticky-footer/>`_
* 清除浮动
* 子选择器
    
    利用父级元素id进行选择
* `图文混排 <http://dabblet.com/gist/4094139>`_
* CSS盒模型
* 垂直居中
* 如何制作三角
* :first-child 和 :last-child
    - 案例 : 圆圈 , padding
* 如果内容可变，就不要设置高度
* 写完页面依次检查
    * 对齐
    * 字体
        * 大小
        * 粗细
        * 颜色
    * 留白
* 邮件
    `Css Inliner Tool <http://templates.mailchimp.com/resources/inline-css/>`_
* 42web
    * HTML中如何引用图片 

    图片上传至七牛，使用外链地址
    * CSS中如何引用图片::

        background:url(/css/_img/xxx)
    * 不要引用站外的图片 
* checkbox 和 radio 的 样式 

  `文字对齐 <http://www.zhangxinxu.com/wordpress/?p=56>`_
* 不要用空格做间距

我们常用的CSS样式
-----------------------------------
* 按钮
    * 功能
    * 强调

设计 
-----------------------------------
* 对齐
* 留白的一致性
* 粗体
* 字号

javascript
-----------------------------------
* 获取时间戳::

    (new Date).getTime()
* 在js中取得当前用户::

    $.current_user
* $$

  例如调用弹窗(可有多个参数)::

    $$('SITE/auth/login')
* require
* $.require
* $.dialog
    * 需要登录调用$.login_dialog(参考submit_project.coffee)
* $.errtip ::

    err = {}

    if xxx:
     err.xxx = "xx"
     if xx :  
        err.xx ="xx"

        if not errtip.set err:
           xxxxx

jQuery
-----------------------------------
* $.extend([deep],target,object)

jQuery 自定义扩展
-----------------------------------
* $.timeago

  接受一个时间戳作为参数,返回距离当前时间描述
* $.isotime
* $.getJSON1
    * jsonp 跨域调用
* $.postJSON1
* $.html 模版

  参考egg_new.coffee

jQuery UI
-----------------------------------
* Accordion
* Datepicker
* Tagit

CoffeeScript
-----------------------------------
* `在页面中直接写coffee <http://coffeescript.org/#scripts>`_

avalon
-----------------------------------
* 命名规则的修改

    "-"改为"_"
* ms_view
* 操作类似view的复用
* view与数据结构的模块划分原则（每一个保存的url对应一个view）
* `$remove <http://limodou.github.io/avalon-learning/zh_CN/event.html>`_
* `$watch <http://limodou.github.io/avalon-learning/zh_CN/watch.html>`_
* 如何定义avalon组建
    * 创建既可以单独使用，也可以在循环中使用的avalon组件

  参考ui_follow.coffee

Firebug
-----------------------------------
* 控制台面板中，点击“保持”按钮，页面重新载入时不清空面板

杂项
-----------------------------------
* `七牛剪裁 <http://developer.qiniu.com/docs/v6/api/reference/fop/image/imageview2.html>`_
* 上传文件
* 上传头像
* 地址选择

Photoshop
-----------------------------------
* `复制psd中的文字 参考psd文字编辑 <http://jingyan.baidu.com/article/fc07f9893db14512ffe5199e.html>`_

工具
-----------------------------------
* Chrome插件 
    * PerfectPixel 
    * Page Ruler 
* Windows
    * Color Picker


后端
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

python
-----------------------------------
* 闭包 
* 正则表达式
* collections
  - defaultdict
* itertools
* enum
  - IntEnum
* enumerate
* time.mktime(time.strptime("2007-03-04 21:08:12", "%Y-%m-%d %H:%M:%S"))
* dateparser
* python 的 新式类与旧式类 ， 以及super的意义

mongodb
-----------------------------------
* find 
    - limit
    - skip
    - sort
* delete
* remove(删除条件)
* save
   - 填充默认值
* upsert

MySQL
-----------------------------------
* get
* mc_get
* mc_get_list

Kv
----------------------------------
* id_by_value
* get
* mc_get

nginx
-----------------------------------

mako
-----------------------------------
* this 比如 this.get_argument('q')
* ${json_encode(xxx)|n}

redis
-----------------------------------
* hset
* set
* zset
* list
* expire 

mongo
-----------------------------------
* 时间用int保存
* mongo默认值需要是一个生成函数
  * pyhton常见的默认值陷阱，以create_time=time()为例

gearman
-----------------------------------

supervisor
-----------------------------------
* 线上服务器如何看异常

tornado
-----------------------------------
* 通过编写 Base View简化业务开发

42web
-----------------------------------
* 新建url页面
* render
* css，js的引用
* merge.conf
* 新建css，js，修改merge.conf需要重启开发服务器
* View的类型
* 分页
* 在页面取得当前用户
* 搜索
* 自动补全
* gearman 异步调用 
* JsOb
* rendermail 发送邮件
* redis key的定义 ， R.
* model 中 使用绝对路径import以防止redis提示key重复定义
* import _env 
* 配置文件 的 定义 与 自适应
* make.py 生成配置文件

开发习惯
----------------------------------
* 修改函数接口后， 用ag查找并修改些调用过的地方
* 函数命名规则 ：名词在前动词在后 ， 常用命名如下

  - user_new 新建
  - user_rm 删除
  - user_dumps 返回一个包含各种相关数据的json对象
  - user_id_list_by_com_id(limit, offset) 查询
  - user_new 新建
  - user_rm 删除
  - user_dumps 返回一个包含各种相关数据的json对象
  - user_id_list_by_com_id(limit, offset) 查询
  - user_id_count_by_com_id
 
  我们通常把user_id作为第一个参数 

开发流程
----------------------------------
* 表单

  #. 编写静态html页面
  #. coffeescript完成交互 
  #. 演示并验收前端页面
  #. 定义 url 和 json数据
  #. 完成ajax保存接口 
  #. 数据回填
  #. 演示并验收
  #. code review
  #. 合并到default 
  #. 上线到开发服务器
  #. 合并到online
  #. 上线到线上服务器 


前端
.................................
* 确认链接都链接到了正确的页面


