# Python 异步框架是如何工作的 [视频]

上一篇博客中我们提到了使用 python selectors 模块和回调的方式来实现一个异步的 tcp echo server，代码大概如下。

```py
import selectors
import socket


class EventLoop:
    def __init__(self, selector=None):
        if selector is None:
            selector = selectors.DefaultSelector()
        self.selector = selector

    def run_forever(self):
        while True:  # EventLoop
            events = self.selector.select()
            for key, mask in events:
                if mask == selectors.EVENT_READ:
                    callback = key.data   # on_read or accept
                    callback(key.fileobj)
                else:
                    callback, msg = key.data
                    callback(key.fileobj, msg)  # callback is _on_write


class TCPEchoServer:
    def __init__(self, host, port, loop):
        self.host = host
        self.port = port
        self._loop = loop
        self.s = socket.socket()

    def run(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(128)
        self.s.setblocking(False)
        self._loop.selector.register(self.s, selectors.EVENT_READ, self._accept)
        self._loop.run_forever()

    def _accept(self, sock):
        conn, addr = sock.accept()
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self._loop.selector.register(conn, selectors.EVENT_READ, self._on_read)

    def _on_read(self, conn):
        msg = conn.recv(1024)
        if msg:
            print('echoing', repr(msg), 'to', conn)
            self._loop.selector.modify(conn, selectors.EVENT_WRITE, (self._on_write, msg))
        else:
            print('closing', conn)
            self._loop.selector.unregister(conn)
            conn.close()

    def _on_write(self, conn, msg):
        conn.sendall(msg)
        self._loop.selector.modify(conn, selectors.EVENT_READ, self._on_read)


event_loop = EventLoop()
echo_server = TCPEchoServer('localhost', 8888, event_loop)
echo_server.run()
```

回调的方式代码结构并不是很好看，回调多了还会形成恶心的回调地狱。这一次我们用协程来重构它，首先我们从生成器和协程讲起，
其实本想直接进入正题的，但是有些读者可能缺少这一块的概念，我这里还是迅速过一遍，我会列出很多链接供你参考。

# 从生成器(Generators)说起

python中生成器是用来生成值的函数。通常函数使用return返回值然后作用域被销毁，再次调用函数会重新执行。但是生成器可以yield一个值之后暂停函数执行，然后控制权交给调用者，之后我们可以恢复其执行并且获取下一个值，我们看一个例子：

```
def simple_gen():
    yield 'hello'
    yield 'world'

gen = simple_gen()
print(type(gen))    # <class 'generator'>
print(next(gen))    # 'hello'
print(next(gen))    # 'world'
```

注意生成器函数调用的时候不会直接返回值，而是返回一个类似于可迭代对象(iterable)的生成器对象(generator object)，我们可以对生成器对象调用next()函数来迭代值，或者使用for循环。
生成器常用来节省内存，比如我们可以使用生成器函数yield值来替代返回一个耗费内存的大序列:

```py
def f(n):
    res = []
    for i in range(n):
        res.append(i)
    return res

def yield_n(n):
    for i in range(n):
        yield i
```

## 什么是基于生成器的协程(coroutine)

上一节讲到了使用使用生成器来从函数中获取数据(pull data)，但是如果我们想发送一些数据呢（push
data）?这时候协程就发挥作用了。yield关键字既可以用来获取数据也可以在函数中作为表达式(在=右边的时候)。我们可以对生成器对象使用send()方法来给函数发送值。这叫做『基于生成器的协程』(generator
based coroutines)。

早期的python 生成器(generator) 可以挂起执行并且保存当前执行的状态，pep 342(Coroutines via Enhanced Generators)
又对其做了增强，生成器可以通过yield 暂停执行和向外返回数据，也可以通过send()向生成器内发送数据，还可以通过throw()向生成器内抛出异常以便随时终止生成器的运行。
（建议感兴趣的读者看看《Fluent Python》14 章和 16章来详细了解生成器、协程、yield from、async/await等概念)

我们先看一个简单的例子:

```py
def coro():
    hello = yield 'hello'    # yield关键字在=右边作为表达式，可以被send值
    yield hello


c = coro()
print(next(c))    # 输出 'hello'，这里调用 next 产出第一个值 'hello'，之后函数暂停
print(c.send('world'))    # 再次调用 send 发送值，此时 hello 变量赋值为 'world', 然后 yield 产出 hello 变量的值 'world'
```

这里发生了什么？和之前一样我们先调用了next()函数，代码执行到yield 'hello'然后我们得到了’hello’之后我们使用了send函数发送了一个值’world’, 它使coro恢复执行并且赋了参数’world’给hello这个变量，接着执行到下一行的yield语句并将hello变量的值’world’返回。所以我们得到了send()方法的返回值’world’。

当我们使用基于生成器的协程(generator based coroutines)时候，术语”generator”和”coroutine”通常表示一个东西，尽管实际上不是。而python3.5以后增加了async/await关键字用来支持原生协程(native coroutines)，我们在后边讨论。


下边是另一个演示协程的例子，注意几个点（我建议你阅读 Fluent Python 相关章节来理解它），如果你对协程等概念不了解，下边的东西看着可能会比较吃力。

- 协程需要使用 send(None) 或者 next(coroutine) 来『预激』(prime) 才能启动
- 在 yield 处协程会暂停执行
- 可以通过 coroutine.send(value) 来给协程发送值
- 协程执行完成后抛出 StopIteration 异常

[协程](./coro.png)

不过通常为了方便，我们会写一个装饰器来预激协程，这样就不用每次都先调用 send(None) 或者 next 了。

```py
from functools import wraps

def coroutine(func):
"""装饰器：向前执行到第一个`yield`表达式，预激`func`"""
@wraps(func)
def primer(*args,**kwargs):  ➊
    gen = func(*args,**kwargs)  ➋
    next(gen)  ➌
    return gen  ➍
return primer
```


# yield from 的含义
yield from 的语义比较复杂，一开始理解会比较吃力，我建议你先阅读下 Fluent Python 16 章协程。 先看下边这个例子:

```
>>> def gen():
...     for c in 'AB':
...         yield c
...     for i in range(1, 3):
...         yield i
...
>>> list(gen())
['A', 'B', 1, 2]

>>> def gen():
...     yield from 'AB'
...     yield from range(1, 3)
...
>>> list(gen())
['A', 'B', 1, 2]
```

python3 引入了 yield from 语法用来链接可迭代对象，引用 pep 380 中的话就是

> “把迭代器当作生成器使用，相当于把子生成器的定义体内联在 yield from 表达式中。此外，子生成器可以执行 return 语句，返回一个值，而返回的值会成为 yield from 表达式的值。”

这样，使用 yield from 就可以起到了『委派』作用，这里我写一个小例子来演示委派生成器的用法，理解它对于后边理解使用协程异步编程非常重要：


```py
def coro1():
    """定义一个简单的基于生成器的协程作为子生成器"""
    word = yield 'hello'
    yield word
    return word


def coro2():
    """委派生成器，起到了调用方和子生成器通道的作用
    委派生成器会在 yield from 表达式处暂停，调用方可以直接发数据发给子生成器，
    子生成器再把产出的值发给调用方。
    子生成器返回后，解释器抛出 StopIteration异常， 并把返回值附加到异常对象上，此时委派生成器恢复
    """
    # 子生成器返回后，解释器抛出 StopIteration 异常，返回值被附加到异常对象上，此时委派生成器恢复
    result = yield from coro1()
    print('coro2 result', result)


def main():  # 调用方，用来演示调用方通过委派生成器可以直接发送值给子生成器
    c2 = coro2()  # 委派生成器
    print(next(c2))   # 委派生成器进入 coro1 执行到第一个 yield 'hello' 产出 'hello'
    print(c2.send('world')) # 委派生成器发送给 coro1，word 赋值为 'world'，之后产出 'world'
    try:
        c2.send(None)  # 发送 None 导致 coro1 结束，返回值赋值给 yield from 表达式的左边的 result，然后输出 coro2 result world
    except StopIteration:
        pass

main()
```


# 使用 Future 对象改写
如果不用回调的方式，如何获取到异步调用的结果呢？python 异步框架中使用到了一个叫做 Future
的对象，当异步调用执行完的时候，用来保存它的结果。

```py
class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for callback in self._callbacks:
            callback(self)

``

Future 对象的 result 用来保存未来的执行结果，set_result 用来设置 result并且运行给 future 对象添加的回调。
注意这里依然无法完全消除回调，但是却可以屏蔽掉业务层代码的回调，后边我们会看到。这里先用 Future 对象来改造之前的
TCPEchoServer，注意代码里的变动。


## Task 对象
上边使用 Future 将函数改造成了 生成器，之前说过生成器需要由 send(None) 或者 next 来启动，遇到 yield 暂停，之后可以通过
send(value) 的方式继续执行。我们创建一个 Task 来管理生成器的执行。




## 参考资料
这里一些参考过的比较好的资料


《Fluent Python》

[深入理解 Python 异步编程](https://mp.weixin.qq.com/s/GgamzHPyZuSg45LoJKsofA)

[从 asyncio 简单实现看异步是如何工作的](https://www.4async.com/2016/02/simple-implement-asyncio-to-understand-how-async-works/)

[Python generators, coroutines, native coroutines and async/await]()

