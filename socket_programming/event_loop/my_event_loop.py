"""

用来了解 event loop 的 python 例子

参考资料：

https://www.4async.com/2016/02/simple-implement-asyncio-to-understand-how-async-works/
https://www.youtube.com/watch?v=ZzfHjytDceU
http://asyncio.readthedocs.io/en/latest/tcp_echo.html
http://scotdoyle.com/python-epoll-howto.html
https://gist.github.com/dtoma/564375673b354397efc5
"""
import selectors
import socket


class EventLoop:

    def __init__(self, selector=None):
        if selector is None:
            selector = selectors.DefaultSelector()
        self._selector = selector

    def add_reader(self, reader, callback):
        try:
            self._selector.register(reader, selectors.EVENT_READ, callback)
        except KeyError:
            pass

    def remove_reader(self, reader):
        try:
            self._selector.unregister(reader)
        except KeyError:
            pass

    def run_forever(self):
        while True:
            events = self._selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


class TCPEchoServer:
    def __init__(self, host, port, loop):
        self.host = host
        self.port = port
        self._loop = loop
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s = s

    def _on_read(self, conn, callback):
        msg = conn.recv(1024)
        if msg:
            print('echoing', repr(msg), 'to', conn)
            conn.sendall(msg)
        else:
            print('closing', conn)
            self._loop.remove_reader(conn)
            conn.close()

    def _accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self._loop.add_reader(conn, self._on_read)

    def run(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)
        self.s.setblocking(False)
        self._loop.add_reader(self.s, self._accept)
        self._loop.run_forever()


event_loop = EventLoop()
echo_server = TCPEchoServer('localhost', 8888, event_loop)
echo_server.run()
