=====================================================================
MongoDb 
=====================================================================

:Author: lzy kzinglzy@gmail.com, tonghs tonghuashuai@gmail.com

简介
=====================================================================
MongoDb是文档型的非关系型数据库，其优势在于查询功能强大，能存储海量数据. 是懒人借以代替SQL型数据库的产品.

在API选择上, 我们用的是基于PyMongo的MongoKit, 并在此基础上进行了小的封装.
所以如果你遇到了问题, 可以去查阅PyMongo或MongoKit的官方文档

基本用法
=====================================================================

创建文档
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在mongo里,用"文档"的概念代替SQL里的"表". 例如, 下面定义了一个UserIm文档::

    class UserIM(Doc):

        structure = dict(
            user_id=int,
            phone=str,
            qq=str,
            weixin=str,
        )

        indexes = [{
            'fields': 'user_id',
            'unique': True
        }]
        default_values = {
            'user_id': 0
        }

其中, UserIm继承自类Doc

structure定义了文档的字段, 接受一个Python字典对象;

indexes定义了索引, 接受一个列表; 

default_values定义了初始化时的默认值.

除此之外, 你还可以添加更多的信息, 这些可以在 `MongoKit document <//https://github.com/namlook/mongokit/wiki>`_ 里找到.

初始化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
初始化一个文档对象可以这么写::

    ui = UserIM()

此时, 所有的文档属性值都会被设为 None , 因为我们并没有给他传递任何值.

这可以通过传递一个字典对象或者JsOB对象来初始化属性值, 如::

    ui = UserIM(dict(user_id=123, phone=456))  # 字典

    ui = UserIM(JsOb(user_id=123, phone=456))  # JsOb 对象

但此时, 其它的没有被初始化的值还是会被设为 None, 若要使我们设置的default_values生效, 可以通过将第二个参数设为True来实现, 如::

    ui = UserIM(dict(user_id=123, phone=456), True)


更新
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
下面我们想更新数据, 如::

    ui = UserIm()
    ui.user_id = 123
    ui.mail = 'abc@gmail.com'
    ui.save()

这将会添加一个user_id为123, mail为abc@gmail.com 的记录.

其中未被赋值的属性会被设为None, 不存在的属性会被忽略. 如果要添加的记录已存在, 那么旧的记录会被替换掉, 否则,会创建一个新的记录.

除此之外, 还有一种更优雅的方式可以实现数据的更新::

    ui = UserIM({'mail': 'abc@gmail.com'})
    user_im.upsert({'user_id': '123'})

这里使用了upsert这个函数, 它的效果和 save 是一样的.但用起来更优雅更简单.


查询
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
常用的查询要用到两个函数::

    UserIM.find(dict(phone=456))

这会返回所有的phone值为456的Python列表. ::

    UserIM.find_one(dict(user_id=123))

这会返回一个用户记录, 其 id 为123.

当然, 还可以添加更多的查询条件来实现复杂的查询, 如::

    UserIM.find(
            {'$or': [{'phone' :456}, {'mail': abc@gmail.com}]},
            limit=10,
            skip=0
            )

如上会返回最多包含10条的, phone 为456或者 mail 为 abc@gmail.com 的记录列表

备份和恢复
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mongodb自带了mongodump和mongorestore这两个工具来实现对数据的备份和恢复。
mongodump能够在Mongodb运行时进行备份，它的工作原理是对运行的Mongodb做查询，然后将所有查到的文档写入磁盘。但是存在的问题时使用mongodump产生的备份不一定是数据库的实时快照，如果我们在备份时对数据库进行了写入操作，则备份出来的文件可能不完全和Mongodb实时数据相等。另外在备份时可能会对其它客户端性能产生不利的影响。

备份::

    mongodump -d SITE -o ~/download/mongobak/SITE/

恢复::
    
    mongorestore -d SITE --directoryperdb ~/download/mongobak/SITE/ --drop

注意: --drop 参数代表恢复前删除原数据

官方文档: http://docs.mongodb.org/manual/core/import-export/

源码
=====================================================================
"源码面前, 了无秘密" -- 侯捷

当你愤怒的发现上面的某些用法不是标准的MongoKit用法时, 就是时候看看源码了::

    /home/zz/42web/z42/web/mongo.py


阅读资料
=====================================================================

`MongoKit document <//https://github.com/namlook/mongokit/wiki>`_

`PyMongo document <//http://api.mongodb.org/python/current>`_

`MongoDB document <//http://docs.mongodb.org/manual>`_

`MongoDB 资料汇总 <http://blog.nosqlfan.com/html/3548.html>`_
