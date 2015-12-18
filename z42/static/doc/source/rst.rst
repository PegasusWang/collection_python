

.. _rst_tutorial: 

==================================================
reStructuredText简明教程
==================================================

:作者: 刘斗 redfork@gmail.com


图形化 web 编辑工具： `rst.ninjs.org <http://rst.ninjs.org/>`_ 

段落
-----------------------


REST 是松散的文本结构，使用预定义的模式描述文章的结构。首先学习最基本的结构：段落。

段落是被空行分割的文字片段，左侧必须对齐（没有空格，或者有相同多的空格）。

  缩进的段落被视为引文。

    继续缩进……

  恢复

恢复


文字样式
-----------------------

最简单的样式是 *斜体* 和 **粗体**.

 * \*斜体\*. 被\*包围的文字是斜体
 * \**粗体**. 被\**包围的文字是粗体


注意: * 两侧必须留有空格, 英文标点符号. 输入法设置为英文标点, 并使用正确的英文标点规范 (逗号, 句号后留一个空格, 引号, 括号两侧留一个空格).

列表
-----------------------

有三种列表: 

 1. 顺序, 

 #. 公告牌, 

 #. 定义. 

列表前后, 以及条目之间必须有空行隔开. 列表下面可以插入任意的内容, 段落, 图片都可以, 只要他们的左侧和列表的第一个文字左对齐.

顺序列表
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

 1. 第 **一** 条

    段落

 #. 第二条

    1. 小条

 #. 第三条


顺序列表 生成:

 1. 第 **一** 条

    段落

 #. 第二条

    1. 小条

 #. 第三条

第二条开始后续的条目用 \# 开头


顺序列表 - 序号
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
第一条的序号不必从 1 开始::

 3. 第三条

 #. 第四条

 7. 重新设定序号

 #. 继续


顺序列表 - 序号 生成:

 3. 第三条

 #. 第四条

 7. 重新设定序号

 #. 继续


顺序列表 - 符号样式
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

符号::

 1. 数字

 a. 小写字母

 A. 大写字母

 i) 小写罗马数字

 (I) 大写罗马数字


顺序列表 - 符号样式 效果

符号:

 1. 数字

 a. 小写字母

 A. 大写字母

 i) 小写罗马数字

 (I) 大写罗马数字



公告牌列表
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

和顺序列表相似, 使用 "*" "+" "-" 代替数字::

 * 列表第一级

   + 第二级

     - 第三级

   + 第二级的另一个项目


公告牌列表 生成:

 * 列表第一级

   + 第二级

     - 第三级

   + 第二级的另一个项目

定义列表
-----------------------

或者叫名词解释更确切::

 *鸡*
   两条腿, 直立行走, 带翅膀, 有头冠的动物.

 *鸭*
   鸡的崇拜者

定义列表生成:

*鸡*
  两条腿, 直立行走, 带翅膀, 有头冠的动物.

*鸭*
  鸡的崇拜者



嵌入程序代码
-----------------------

如果需要嵌入大段的程序代码(SQL, 业务逻辑设置, 配置文件等), 在段落末尾添加两个':'. 代码的左侧必须缩进, 代码引用到没有缩进的行为止. 例如::

 如果数据库有问题, 执行下面的 SQL::

  # Dumping data for table `item_table`

  INSERT INTO item_table VALUES (
    0000000001, 0, 'Manual', '', '0.18.0', 
    'This is the manual for Mantis version 0.18.0.\r\n\r\nThe Mantis manual is modeled after the [url=http://www.php.net/manual/en/]PHP Manual[/url]. It is authored via the \\"manual\\" module in Mantis CVS.  You can always view/download the latest version of this manual from [url=http://mantisbt.sourceforge.net/manual/]here[/url].',
    '', 1, 1, 20030811192655);


嵌入程序代码生成:

如果数据库有问题, 执行下面的 SQL::

  # Dumping data for table `item_table`
  INSERT INTO item_table VALUES (
    0000000001, 0, 'Manual', '', '0.18.0', 
    'This is the manual for Mantis version 0.18.0.\r\n\r\nThe Mantis manual is modeled after the [url=http://www.php.net/manual/en/]PHP Manual[/url]. It is authored via the \\"manual\\" module in Mantis CVS.  You can always view/download the latest version of this manual from [url=http://mantisbt.sourceforge.net/manual/]here[/url].',
    '', 1, 1, 20030811192655);


嵌入程序代码 续
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果没有合适的段落添加 \::, 也可以在一个空行上添加, 这个双冒号行被忽略::

  ::

  #
  # Dumping data for table `item_table`
  #

  INSERT INTO item_table VALUES (
    0000000001, 0, 'Manual', '', '0.18.0', 
    'This is the manual for Mantis version 0.18.0.\r\n\r\nThe Mantis manual is modeled after the [url=http://www.php.net/manual/en/]PHP Manual[/url]. It is authored via the \\"manual\\" module in Mantis CVS.  You can always view/download the latest version of this manual from [url=http://mantisbt.sourceforge.net/manual/]here[/url].',
    '', 1, 1, 20030811192655);


嵌入程序代码 续 生成:

::

  #
  # Dumping data for table `item_table`
  #

  INSERT INTO item_table VALUES (
    0000000001, 0, 'Manual', '', '0.18.0', 
    'This is the manual for Mantis version 0.18.0.\r\n\r\nThe Mantis manual is modeled after the [url=http://www.php.net/manual/en/]PHP Manual[/url]. It is authored via the \\"manual\\" module in Mantis CVS.  You can always view/download the latest version of this manual from [url=http://mantisbt.sourceforge.net/manual/]here[/url].',
    '', 1, 1, 20030811192655);




程序引用体例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

可以 用 `.. code-block::` 追加各种语法高亮声明::


    .. code-block:: python
        :linenos:

        def foo():
            print "Love Python, Love FreeDome"
            print "E文标点,.0123456789,中文标点,. "


效果:

.. code-block:: python
    :linenos:

    def foo():
        print "Love Python, Love FreeDome"
        print "E文标点,.0123456789,中文标点,. "


外部包含::

    .. literalinclude:: example.py
        :language: python


效果:

.. literalinclude:: example.py
    :language: python




章节
-----------------------

章节是文章的主体结构, 分为 **标题 章 节 小节** 等. 定义章节的方式是在行的下面添加 '=======', 比如::

  标题
  ====

  章
  --

  节
  ~~

  小节
  ####


说明 [1]_:

 1. '====' 至少和文字行一样长, 更长也行

 #. 相同级别必须使用统一的符号, 否则会被识别为更小的级别
 
 #. = - ~ ` : ' " ^ _ * _ # < > 
    这些符号都可以, 级别足够多了.

.. [1] 由于幻灯片系统的限制, 效果无法在幻灯片内演示


标题
-----------------------

标题和章节在结构上的作用相同, 但是可能有不同的显示格式. 标题的区别是在章节的上方也加上 '====' 行::

  ====
  标题
  ====

  -----------
  第一章 概述
  -----------


表格
-----------------------

普通表格 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

 +------------+------------+-----------+
 | Header 1   | Header 2   | Header 3  |
 +============+============+===========+
 | body row 1 | column 2   | column 3  |
 +------------+------------+-----------+
 | body row 2 | Cells may span columns.|
 +------------+------------+-----------+
 | body row 3 | Cells may  | - Cells   |
 +------------+ span rows. | - contain |
 | body row 4 |            | - blocks. |
 +------------+------------+-----------+


普通表格 生成:

 +------------+------------+-----------+
 | Header 1   | Header 2   | Header 3  |
 +============+============+===========+
 | body row 1 | column 2   | column 3  |
 +------------+------------+-----------+
 | body row 2 | Cells may span columns.|
 +------------+------------+-----------+
 | body row 3 | Cells may  | - Cells   |
 +------------+ span rows. | - contain |
 | body row 4 |            | - blocks. |
 +------------+------------+-----------+

简单表格
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*注意:* 表格包含中文时,基本无法对齐,,,

::

 =====  =====  ====== 
    Inputs     Output 
 ------------  ------ 
   A      B    A or B 
 =====  =====  ====== 
 False  False  False 
 True   False  True 
 False  True   True 
 True   True   True 
 =====  =====  ======

简单表格  生成:

 =====  =====  ====== 
    Inputs     Output 
 ------------  ------ 
   A      B    A or B 
 =====  =====  ====== 
 False  False  False 
 True   False  True 
 False  True   True 
 True   True   True 
 =====  =====  ======


CSV 表格
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  .. csv-table:: Frozen Delights!
   :header: "Treat", "Quantity", "Description"
   :widths: 15, 10, 30

   "Albatross", 2.99, "On a stick!"
   "Crunchy Frog", 1.49, "If we took the bones out, it wouldn't be
   crunchy, now would it?"
   "Gannet Ripple", 1.99, "On a stick!"


CSV 表格生成:

.. csv-table:: Frozen Delights!
   :header: "Treat", "Quantity", "Description"
   :widths: 15, 10, 30

   "Albatross", 2.99, "On a stick!"
   "Crunchy Frog", 1.49, "If we took the bones out, it wouldn't be
   crunchy, now would it?"
   "Gannet Ripple", 1.99, "On a stick!"

列表表格
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

 .. list-table:: Frozen Delights!
   :widths: 15 10 30
   :header-rows: 1

   * - Treat
     - Quantity
     - Description
   * - Albatross
     - 2.99
     - On a stick!
   * - Crunchy Frog
     - 1.49
     - If we took the bones out, it wouldn't be
       crunchy, now would it?
   * - Gannet Ripple
     - 1.99
     - On a stick!


列表表格 生成:

.. list-table:: Frozen Delights!
   :widths: 15 10 30
   :header-rows: 1

   * - Treat
     - Quantity
     - Description
   * - Albatross
     - 2.99
     - On a stick!
   * - Crunchy Frog
     - 1.49
     - If we took the bones out, it wouldn't be
       crunchy, now would it?
   * - Gannet Ripple
     - 1.99
     - On a stick!



rST排版技巧
-----------------------

跨章节指引
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- 行文中,经常要对其它章节进行指引,在 html 中对应的就是 锚点链接
- rST 中提供了非常优雅的解决:
    - 使用通用元素定义
    - 比如説:

::

  各个章节的首页一般是 index.rst
  头一行,习惯性加个聲明:
  .. _chapter6index:

  那么,在其它任意文本中,随时可以使用:
  :ref:`构建 buzz <chapter6index>` 
  来生成一个指向第二章 首页的链接!



插图/表格指代
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- 行文中,经常对指定插图/表格 进行指代
- rST 中提供了非常优雅的解决:
    - 进行通用元素定义
    - 比如说

::

  .. _fig_0601:
  .. figure:: _static/figs/magic-2.png

     插图 6-1 神奇的2


然后,就可以在任意地方使用 :ref:`fig_0601` 来指代,
实际输出的就是 "插图 6-1 神奇的2"


.. _fig_0601:
.. figure:: _static/figs/magic-2.png

   插图 6-1 神奇的2



上下标号
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

有时要进行数学/化学的表示,在 html 中就需要上/下标( `<sub>` , `<sup>`) 的表达,
rST 中当然也有::

  H\ :sub:`2`\ O
  E = mc\ :sup:`2`

效果:

H\ :sub:`2`\ O

E = mc\ :sup:`2`


.. note:: 注意:

  这里的 \ 只是为了制造语法空间,输出时,是没有空格的了,,,



段落层次约定
-----------------------

使用 

::

    共分4级    
    =======================
    大标题
    =======================


    -----------------------    
    小标题
    -----------------------    


    ^^^^^^^^^^^^^^^^^^^^^^^    
    二级标题
    ^^^^^^^^^^^^^^^^^^^^^^^    


    """""""""""""""""""""""    
    三级标题
    """""""""""""""""""""""    



再小，就使用列表!:

    - 列表项目1    
    - 列表项目2
    - ...






