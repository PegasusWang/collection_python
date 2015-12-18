

.. _shell_tutorial: 

==================================================
Unix/Linux 常用 shell 命令
==================================================

:作者: 王然 kxxoling@gmail.com

简介
---------------------------------------------

shell 是 Unix/Linux 上常见的用户与计算机的交互接口，根据用户输入执行系统命令。
现如今，主流 Linux 发行版中默认的 shell 多是 bash。

开发服务器上使用的 shell 也是 bash，并安装了一些第三方命令和自己编写的批处理命令。


常用 bash 命令
----------------------------------------------

* table 键自动补全
* ls 列出目录
* ls -al 使用格式化列出隐藏文件
* pwd 显示当前目录
* cd <dir> 切换到 dir 目录
* cd 切换到 home 目录
* cd .. 切换到父目录
* mkdir <dir> 创建目录
* touch <file> 创建文件
* cat <file> 显示文件内容
* less <file> 逐页显示文件内容
* more <file>
* head <file> 显示文件头 10 行
* tail <file> 显示文件后 10 行
* tail -f <file> 从后 10 行开始查看文件内容
* ctrl+c 结束程序
* ctrl+z 停止当前程序，可使用 fg 恢复
* ctrl+w 删除当前行中文字
* ctrl+u 删除整行文字
* ctrl+a/e 将光标移动至行首/尾
* ctrl+r 搜索最近使用的命令
* bg 列出已停止或者后台程序
* fg 将最近作业带到前台
* locate <file> 查找某个文件所在位置


常用第三方命令
----------------------------------------------


tree 以树形显示当前目录结构

* tree 以树形结构显示当前目录下所有文件和目录
* tree -d 仅显示目录
* tree -L <num> 限制目录的最大深度

ag 搜索

* ag <something> 在目录所有文件中寻找 something
* ag <something> <--python> 在所有 Python 文件中搜索 something

`autojump <https://github.com/joelthelion/autojump>`

* j <dir> 根据最近工作目录记录跳转到最合适的位置。


其它批处理命令
----------------------------------------------

:ref:`42qucc_tutorial`

deltmp
递归删除目录中所有 vim 临时文件。
