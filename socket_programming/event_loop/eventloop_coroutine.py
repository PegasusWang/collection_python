import selectors
import socket


# TODO 尝试模仿一个简易版的 Future  和 Task
"""
参考：
https://www.jianshu.com/p/b5e347b3a17c
http://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/
http://masnun.com/2015/11/20/python-asyncio-future-task-and-the-event-loop.html
https://www.4async.com/2016/02/simple-implement-asyncio-to-understand-how-async-works/
[深入理解python异步编程](https://mp.weixin.qq.com/s/GgamzHPyZuSg45LoJKsofA)
http://github.com/denglj/aiotutorial

很多概念：
协程
Future
Task
EventLoop
"""


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

    def __iter__(self):
        yield self
        return self.result


class Task:
    """管理生成器的执行"""

    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:  # 把当前 future 的结果发送给协程作为 yield from 表达式的值，同时执行到下一个 future 处
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)


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

        while True:
            conn, addr = yield from self.accept()
            msg = yield from self.read(conn)
            if msg:
                yield from self.sendall(conn, msg)
            else:
                conn.close()

    def accept(self):
        f = Future()

        def on_accept():
            conn, addr = self.s.accept()
            print('accepted', conn, 'from', addr)
            conn.setblocking(False)
            f.set_result((conn, addr))  # accept 的 result 是接受连接的新对象 conn, addr
        self._loop.selector.register(self.s, selectors.EVENT_READ, on_accept)
        conn, addr = yield from f  # 委派给 future 对象，直到 future 执行了 socket.accept() 并且把 result 返回
        self._loop.selector.unregister(self.s)
        return conn, addr

    def read(self, conn):
        f = Future()

        def on_read():
            msg = conn.recv(1024)
            f.set_result(msg)
        self._loop.selector.register(conn, selectors.EVENT_READ, on_read)
        msg = yield from f
        return msg

    def sendall(self, conn, msg):
        f = Future()

        def on_write():
            conn.sendall(msg)
            f.set_result(None)
            self._loop.selector.unregister(conn)
            conn.close()
        self._loop.selector.modify(conn, selectors.EVENT_WRITE, on_write)
        yield from f


class EventLoop:
    def __init__(self, selector=None):
        if selector is None:
            selector = selectors.DefaultSelector()
        self.selector = selector

    def create_task(self, coro):
        return Task(coro)

    def run_forever(self):
        while 1:
            events = self.selector.select()
            for event_key, event_mask in events:
                callback = event_key.data
                callback()


event_loop = EventLoop()
echo_server = TCPEchoServer('localhost', 8888, event_loop)
task = Task(echo_server.run())
event_loop.run_forever()
