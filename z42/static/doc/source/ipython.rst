=======

.. _vps_tutorial: 

==================================================
IPython 用法
==================================================

:作者: 王然 kxxoling@gmail.com

启动
============

启动IPython就是运行可执行文件ipython。你会看到一个提示符，如果你曾经玩过标准Python命令行提示符，你会发现这个有点儿不同::

    [jjones@cerberus ~]$ /usr/local/python24/bin/ipython 
    Python 2.4 (#2, Nov 30 2004, 09:22:54) 
    Type "copyright", "credits" or "license" for more information. 

    IPython 0.6.6 -- An enhanced Interactive Python. 
    ? -> Introduction to IPython's features. 
    %magic -> Information about IPython's 'magic' % functions. 
    help -> Python's own help system. 
    object? -> Details about 'object'. ?object also works, ?? prints more. 

    In [1]: 

要退出IPython（Linux系统上）就输入Ctrl-D（会要求你确认），也可以输入Exit或Quit（注意大小写）退出而不需要确认。 

特性
============

Magic
------------

IPython有一些"magic"关键字::

    %Exit, %Pprint, %Quit, %alias, %autocall, %autoindent, %automagic, 
    %bookmark, %cd, %color_info, %colors, %config, %dhist, %dirs, %ed, 
    %edit, %env, %hist, %logoff, %logon, %logstart, %logstate, %lsmagic, 
    %macro, %magic, %p, %page, %pdb, %pdef, %pdoc, %pfile, %pinfo, %popd, 
    %profile, %prun, %psource, %pushd, %pwd, %r, %rehash, %rehashx, %reset, 
    %run, %runlog, %save, %sc, %sx, %system_verbose, %unalias, %who, 
    %who_ls, %whos, %xmode 

IPython 会检查传给它的命令是否包含magic关键字。如果命令是一个magic关键字，IPython就自己来处理。如果不是magic关键字，就交给 Python（标准解释器）去处理。如果automagic打开（默认），你不需要在magic关键字前加%符号。相反，如果automagic是关闭的，则%是必须的。在命令提示符下输入命令magic就会显示所有magic关键字列表以及它们的简短的用法说明。良好的文档对于一个软件的任何一部分来说都是重要的，从在线IPython用户手册到内嵌文档（%magic），IPython当然不会在这方面有所缺失。 

Tab自动补全
------------

IPython一个非常强大的功能是tab自动补全。如果你对Python很了解，可能会想，标准Python交互式解释器也可以tab自动补全啊。你要做的只是:: 

    [jjones@cerberus ~]$ /usr/local/python24/bin/python 
    Python 2.4 (#2, Nov 30 2004, 09:22:54) 
    [GCC 3.4.2 20041017 (Red Hat 3.4.2-6.fc3)] on linux2 
    Type "help", "copyright", "credits" or "license" for more information. 
    >>> import rlcompleter, readline 
    >>> readline.parse_and_bind('tab: complete') 
    >>> 

是的，标准Python交互式解释器和IPython都支持“普通”自动补全和菜单补全。使用自动补全，你要先输入一个匹配模型，然后按Tab键。如果是“普通”自动补全模式（默认），Tab后会： 

* 匹配模型按最大匹配展开。 
* 列出所有匹配的结果。 

例如:: 

    In [1]: import os 
    In [2]: os.po 
    os.popen os.popen2 os.popen3 os.popen4 
    In [2]: os.popen 

输入os.po然后按Tab键，os.po被展开成os.popen（就象在In [2]:提示符显示的那样），并显示os所有以po开头的模块，类和函数，它们是popen，popen2， popen3和popen4。 

菜单补全稍有不同。关闭默认Tab补全，使用菜单补全，你需要修改配置文件$HOME/.ipython/ipythonrc。注释掉： 
    readline_parse_and_bind tab: complete 

取消注释: 
    readline_parse_and_bind tab: menu-complete 

不同于“普通”自动补全的显示当前命令所有匹配列表，菜单补全会随着你每按一次Tab键而循环显示匹配列表中的项目。例如::

    In [1]: import os 
    In [2]: os.po 

结果是： 

    In [3]: os.popen 

接下来每次按Tab键就会循环显示匹配列表中的其它项目：popen2，popen3，popen4，最后回到po。菜单补全模式下查看所有匹配列表的快捷键是Ctrl-L::

    In [2]: os.po 
    os.popen os.popen2 os.popen3 os.popen4 
    In [2]: os.po 

自省
------------

Python有几个内置的函数用于自省。IPython不仅可以调用所有标准Python函数，对于那些Python shell内置函数同样适用。典型的使用标准Python shell进行自省是使用内置的dir()函数::

    >>> import SimpleXMLRPCServer 
    >>> dir(SimpleXMLRPCServer.SimpleXMLRPCServer) 
    ['__doc__', '__init__', '__module__', '_dispatch', 
    '_marshaled_dispatch', 'address_family', 'allow_reuse_address', 
    'close_request', 'fileno', 'finish_request', 'get_request', 
    'handle_error', 'handle_request', 'process_request', 
    'register_function', 'register_instance', 
    'register_introspection_functions', 'register_multicall_functions', 
    'request_queue_size', 'serve_forever', 'server_activate', 'server_bind', 
    'server_close', 'socket_type', 'system_listMethods', 
    'system_methodHelp', 'system_methodSignature', 'system_multicall', 
    'verify_request'] 

嗯，非常棒。事实上非常实用。几年来我一直这么做，对此非常满意。这是一个漂亮的列表，包含了 SimpleXMLRPCServer.SimpleXMLRPCServer的所有方法，类，模块等等。因为dir()是一个内置函数，在 IPython中也能很好的使用它们。但是IPython的操作符?和??功能还要强大::

        In [1]: import SimpleXMLRPCServer 

        In [2]: ? SimpleXMLRPCServer.SimpleXMLRPCServer 
        Type: classobj 
        String Form: SimpleXMLRPCServer.SimpleXMLRPCServer 
        Namespace: Interactive 
        File: /usr/local/python24/lib/python2.4/SimpleXMLRPCServer.py 
        Docstring: 
        Simple XML-RPC server. 

        Simple XML-RPC server that allows functions and a single instance 
        to be installed to handle requests. The default implementation 
        attempts to dispatch XML-RPC calls to the functions or instance 
        installed in the server. Override the _dispatch method inherited 
        from SimpleXMLRPCDispatcher to change this behavior. 

        Constructor information: 
        Definition: SimpleXMLRPCServer.SimpleXMLRPCServer(self, addr, 
        requestHandler=, logRequests=1) 

? 操作符会截断长的字符串。相反，?? 不会截断长字符串，如果有源代码的话还会以语法高亮形式显示它们。 

历史
-----------

当你在IPython shell下交互的输入了大量命令，语句等等，就象这样::

    In [1]: a = 1 

    In [2]: b = 2 

    In [3]: c = 3 

    In [4]: d = {} 

    In [5]: e = [] 

    In [6]: for i in range(20): 
    ...: e.append(i) 
    ...: d[i] = b 
    ...: 

你可以快速查看那些输入的历史记录::

    In [7]: hist 
    1: a = 1 
    2: b = 2 
    3: c = 3 
    4: d = {} 
    5: e = [] 
    6: 
    for i in range(20): 
    e.append(i) 
    d[i] = b 

要去掉历史记录中的序号（这里是1至6），使用命令hist -n::

    In [8]: hist -n 
    a = 1 
    b = 2 
    c = 3 
    d = {} 
    e = [] 
    for i in range(20): 
    e.append(i) 
    d[i] = b 

这样你就可以方便的将代码复制到一个文本编辑器中。要在历史记录中搜索，可以先输入一个匹配模型，然后按Ctrl-P。找到一个匹配后，继续按Ctrl-P会向后搜索再上一个匹配，Ctrl-N则是向前搜索最近的匹配。 


编辑 
===========

当在Python提示符下试验一个想法时，经常需要通过编辑器修改源代码（甚至是反复修改）。在IPython下输入edit就会根据环境变量$EDITOR调用相应的编辑器。如果$EDITOR为空，则会调用vi（Unix）或记事本（Windows）。要回到IPython提示符，直接退出编辑器即可。如果是保存并退出编辑器，输入编辑器的代码会在当前名字空间下被自动执行。如果你不想这样，使用edit -x。如果要再次编辑上次最后编辑的代码，使用edit -p。在上一个特性里，我提到使用hist -n可以很容易的将代码拷贝到编辑器。一个更简单的方法是edit加Python列表的切片（slice）语法。假定hist输出如下::

    In [29]: hist 
    1 : a = 1 
    2 : b = 2 
    3 : c = 3 
    4 : d = {} 
    5 : e = [] 
    6 : 
    for i in range(20): 
    e.append(i) 
    d[i] = b 

    7 : %hist 

现在要将第4，5，6句代码导出到编辑器，只要输入： 

    edit 4:7 


Debugger接口 
-------------

IPython 的另一特性是它与Python debugger的接口。在IPython shell下输入magic关键字pdb就会在产生一个异常时自动开关debugging功能。在自动pdb呼叫启用的情况下，当Python遇到一个未处理的异常时Python debugger就会自动启动。你在debugger中的当前行就是异常发生的那一行。IPython的作者说有时候当他需要在某行代码处debug时，他会在开始debug的地方放一个表达式1/0。启用pdb，在IPython中运行代码。当解释器处理到1/0那一行时，就会产生一个 ZeroDivisionError异常，然后他就在指定的代码处被带到一个debugging session中了。 

运行 
-------------
有时候当你在一个交互式shell中时，如果可以运行某个源文件中的内容将会很有用。运行magic关键字run带一个源文件名就可以在IPython解释器中运行一个文件了（例如run <源文件> <运行源文件所需参数>）。参数主要有以下这些： 

* -n 阻止运行源文件代码时__name__变量被设为"__main__"。这会防止 ::

    if __name__ == "__main__": 

  块中的代码被执行 

* -i 源文件就在当前IPython的名字空间下运行而不是在一个新的名字空间中。如果你需要源代码可以使用在交互式session中定义的变量就会很有用。 

* -p 使用Python的profiler模块运行并分析源代码。使用该选项代码不会运行在当前名字空间。 


宏
-------------

宏允许用户为一段代码定义一个名字，这样你可以在以后使用这个名字来运行这段代码。就象在magic关键字edit中提到的，列表切片法也适用于宏定义。假设有一个历史记录如下::

    In [3]: hist 
    1: l = [] 
    2: 
    for i in l: 
    print i 

你可以这样来定义一个宏： 

    In [4]: macro print_l 2 
    Macro `print_l` created. To execute, type its name (without quotes). 
    Macro contents: 
    for i in l: 
    print i 

运行宏:: 

    In [5]: print_l 
    Out[5]: Executing Macro... 

在这里，列表l是空的，所以没有东西被输出。但这其实是一个很强大的功能，我们可以赋予列表l某些实际值，再次运行宏就会看到不同的结果::

    In [6]: l = range(5) 

    In [7]: print_l 
    Out[7]: Executing Macro... 
    0 
    1 
    2 
    3 
    4 

当运行一个宏时就好象你重新输入了一遍包含在宏print_1中的代码。它还可以使用新定义的变量l。由于Python语法中没有宏结构（也许永远也不会有），在一个交互式shell中它更显得是一个有用的特性。 

环境（Profiles） 
===================================

就象早前提到的那样，IPython安装了多个配置文件用于不同的环境。配置文件的命名规则是ipythonrc-。要使用特定的配置启动IPython，需要这样 :: 

    ipython -p 

一个创建你自己环境的方法是在$HOME/.ipython目录下创建一个IPython配置文件，名字就叫做ipythonrc- ，这里是你想要的环境的名字。如果你同时进行好几个项目，而这些项目又用到互不相同的特殊的库，这时候每个项目都有自己的环境就很有用了。你可以为每个项目建立一个配置文件，然后在每个配置文件中import该项目中经常用到的模块。 

使用操作系统的Shell 
=================================

使用默认的IPython配置文件，有几个Unix Shell命令（当然，是在Unix系统上），cd，pwd和ls都能象在bash下一样工作。运行其它的shell命令需要在命令前加!或!!。使用magic关键字%sc和%sx可以捕捉shell命令的输出。 

pysh环境可以被用来替换掉shell。使用-p pysh参数启动的IPython，可以接受并执行用户$PATH中的所有命令，同时还可以使用所有的Python模块，Python关键字和内置函数。例如，我想要创建500个目录，命名规则是从d_0_d到d_500_d（译注：呵呵，作者这里犯了个小小的计算错误，你能看出来吗），我可以使用-p pysh启动IPython，然后就象这样::

    jjones@cerberus[foo]|2> for i in range(500): 
    |.> mkdir d_${i}_d 
    |.> 

这就会创建500个目录::

    jjones@cerberus[foo]|8> ls -d d* | wc -l 
    500 

注意这里混合了Python的range函数和Unix的mkdir命令。 

注意，虽然ipython -p pysh提供了一个强大的shell替代品，但它缺少正确的job控制。在运行某个很耗时的任务时按下Ctrl-z将会停止IPython session而不是那个子进程。 

问题和方法 
==============

虽然作为标准Python shell的替换，IPython总的来说很完美。还是有两个问题给我带来了一些麻烦。感谢IPython的开发者，这两个问题都可以通过配置来解决，每个配置都有清晰的文档。 

第一个问题是关于颜色的。在我的一个系统上，我使用的是一个白色背景的xterm。当我使用?和??查询一个对象或模块的信息时，对象的定义会被显示，但看起来好象那些参数丢失了。那是因为在构造函数中的的参数默认显示为白色。我的解决办法是在IPython shell中输入colors LightBG。 

第二个问题是关于自动缩进和代码粘贴的。如果autoindent被启用，IPython会对我粘贴的已排好缩进的代码再次应用缩进。例如下面的代码::

    for i in range(10): 
    for j in range(10): 
    for k in range(10): 
    pass 

会变成::

    for i in range(10): 
    for j in range(10): 
    for k in range(10): 
    pass 

在这里它并不是个问题，因为在它自身中缩进都保持一致。在其它一些情况下（例子一下子举不出来了），可能会成为真正的问题。可以使用magic关键字autoindent来开关自动缩进，告诉IPython不要添加多余的缩进──就象在vim中设置粘贴set paste一样。 

结论 
==============

IPython 并不是囗囗性的，也不是完全创新的。Tab自动补全，历史记录搜索，配置环境，配置文件等都早已在其它shells中存在有些年头了。Python拥有各种级别的自省能力也有一段时间了。但IPython把来自成熟的Unix shell，标准Python shell以及Python语言中的一些最强大的功能整合到了一起。产生出了一个强大的令人难以置信的性能增强工具，我想我会很乐意在接下来的几年中一直使用它。套用阿基米德的话来说，给我一个强大而又灵活的文本编辑器（vim），一个交互式shell（IPython）以及一个语言（Python），我就能撬动整个世界。

