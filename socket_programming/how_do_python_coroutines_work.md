# callback-based async
# non-blocking sockets
# callbacks
# event loop
# coroutines

# 用 Python3 实现异步的 http server

首先用 socket 实现一个简单的 http 请求，代码如下：

```
import socket
import time


def get(path):
    s = socket.socket()
    s.connect(('localhost', 5000))

    request = 'GET {} HTTP/1.0\r\n\r\n'.format(path)
    s.send(request.encode())

    chunks = []
    while True:
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = (b''.join(chunks)).decode()
            print(body)
            return


start = time.time()
get('/1')
get('/2')
print(time.time() - start)
```

通过模拟 http 协议我们实现了一个简单的同步爬虫，执行下发现大概耗时 0.02 秒。
下边我们把 socket 改成异步的，在此之前建议你看下 python3 提供的 selectors 模块，
在之前的 select 模块的基础上提供了高层抽象的 IO 多路复用：


    import socket
    import time
    from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


    selector = DefaultSelector()
    n_jobs = 0


    def get(path):
        global n_jobs
        n_jobs += 1
        s = socket.socket()
        s.setblocking(False)    # 非阻塞模式
        try:
            s.connect(('localhost', 5000))
        except BlockingIOError:
            pass

        def callback(): return connected(s, path)
        selector.register(s.fileno(), EVENT_WRITE, data=callback)


    def connected(s, path):
        selector.unregister(s.fileno())
        request = 'GET {} HTTP/1.0\r\n\r\n'.format(path)
        s.send(request.encode())

        chunks = []

        def callback(): return readable(s, chunks)
        selector.register(s.fileno(), EVENT_READ, callback)


    def readable(s, chunks):
        global n_jobs
        selector.unregister(s.fileno())
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)

            def callback(): return readable(s, chunks)
            selector.register(s.fileno(), EVENT_READ, callback)
        else:
            body = (b''.join(chunks)).decode()
            print(body)
            n_jobs -= 1


    start = time.time()
    get('/1')
    get('/2')

    while n_jobs:
        events = selector.select()
        for key, mask in events:
            callback_func = key.data
            callback_func()

    print(time.time() - start)

好了，运行下这个文件，你会发现是异步执行的。
但是还记得著名的回调地狱吗，这里我们写了很多 callback 函数，比较恶心。
在 python3 中， 基于 croutine，Future，Task 等实现了用同步的方式写异步代码。
来看怎么一步步改造它，首先我们用 Future 对象替换之前的回调函数注册给 selector 的 data。

    import socket
    import time
    from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


    selector = DefaultSelector()
    num_tasks = 0

    class Future:
        """代表pending 的 events"""
        def __init__(self):
            self.callbacks = []

        def resolve(self):
            for callback in self.callbacks:
                callback()


    def get(path):
        global num_tasks
        num_tasks += 1
        s = socket.socket()
        s.setblocking(False)    # 非阻塞模式
        try:
            s.connect(('localhost', 5000))
        except BlockingIOError:
            pass

        request = 'GET {} HTTP/1.0\r\n\r\n'.format(path)

        def callback(): return connected(s, request)
        f = Future()
        f.callbacks.append(callback)
        selector.register(s.fileno(), EVENT_WRITE, data=f)    # data 是 Future 对象


    def connected(s, request):
        selector.unregister(s.fileno())
        # socket 可写
        s.send(request.encode())

        chunks = []

        def callback(): return readable(s, chunks)
        f = Future()
        f.callbacks.append(callback)
        selector.register(s.fileno(), EVENT_READ, data=f)


    def readable(s, chunks):
        global num_tasks
        # s is readable
        selector.unregister(s.fileno())
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)

            def callback(): return readable(s, chunks)
            f = Future()
            f.callbacks.append(callback)
            selector.register(s.fileno(), EVENT_READ, data=f)
        else:
            body = (b''.join(chunks)).decode()
            print(body)
            num_tasks -= 1


    start = time.time()
    get('/1')
    get('/2')

    while num_tasks:
        events = selector.select()
        for event, mask in events:
            future = event.data
            future.resolve()


    print(time.time() - start)

这里的改动就是把所有之前注册的回调函数改成了 Future 对象，最后 while 循环里统一调用了 resolve 方法来执行所有注册的回调。
嗯，似乎并没有改善代码，反而越写越乱了。这个时候 python 的生成器派上用场了
让我们删除 callback 改成协程

    def get(path):
        global num_tasks
        num_tasks += 1
        s = socket.socket()
        s.setblocking(False)    # 非阻塞模式
        try:
            s.connect(('localhost', 5000))
        except BlockingIOError:
            pass

        request = 'GET {} HTTP/1.0\r\n\r\n'.format(path)

        f = Future()
        selector.register(s.fileno(), EVENT_WRITE, data=f)    # data 是 Future 对象

        # 需要停止直到 s 可写
        yield f

        selector.unregister(s.fileno())
        # socket 可写
        s.send(request.encode())

        chunks = []

        def callback(): return readable(s, chunks)
        f = Future()
        f.callbacks.append(callback)
        selector.register(s.fileno(), EVENT_READ, data=f)


我们删掉了 callback 改成了协程，这个时候 get 函数返回了生成器 generator，
运行下你会发现什么都没发生？为什么，因为协程需要 next 来启动（prime）它，
我们需要一个对象来驱动协程，也就是调用 next 方法。在很多 python 异步框架中都实现了一个 Task 对象驱动协程

    """
    Future
    generators
    Task
    """

    import socket
    import time
    from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


    selector = DefaultSelector()
    num_tasks = 0

    class Future:
        """代表pending 的 events"""
        def __init__(self):
            self.callbacks = []

        def resolve(self):
            for callback in self.callbacks:
                callback()


    class Task:
        def __init__(self, gen):
            self.gen = gen
            self.step()    # 第一次驱动协程执行

        def step(self):
            try:
                f = next(self.gen)
            except StopIteration:
                return
            f.callbacks.append(self.step)

    def get(path):
        global num_tasks
        num_tasks += 1
        s = socket.socket()
        s.setblocking(False)    # 非阻塞模式
        try:
            s.connect(('localhost', 5000))
        except BlockingIOError:
            pass

        request = 'GET {} HTTP/1.0\r\n\r\n'.format(path)

        f = Future()
        selector.register(s.fileno(), EVENT_WRITE, data=f)    # data 是 Future 对象

        # 需要停止直到 s 可写
        yield f

        selector.unregister(s.fileno())
        # socket 可写
        s.send(request.encode())

        chunks = []

        while True:
            f = Future()
            selector.register(s.fileno(), EVENT_READ, data=f)

            yield f
            # when resume , s is readable
            selector.unregister(s.fileno())
            chunk = s.recv(1000)
            if chunk:
                chunks.append(chunk)

            else:
                body = (b''.join(chunks)).decode()
                print(body)
                num_tasks -= 1
                return


    start = time.time()
    Task(get('/1'))    # get 返回协程，用 Task 驱动
    Task(get('/2'))

    while num_tasks:
        events = selector.select()
        for event, mask in events:
            future = event.data
            future.resolve()


    print(time.time() - start)
