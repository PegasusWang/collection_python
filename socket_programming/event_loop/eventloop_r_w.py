# -*- coding: utf-8 -*-

import selectors
import socket


class EventLoop:

    def __init__(self, selector=None):
        if selector is None:
            selector = selectors.DefaultSelector()
        self.selector = selector

    def run_forever(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                if mask == selectors.EVENT_READ:
                    callback = key.data
                    callback(key.fileobj)
                else:
                    callback, msg = key.data
                    callback(key.fileobj, msg)


class TCPEchoServer:
    def __init__(self, host, port, loop):
        self.host = host
        self.port = port
        self._loop = loop
        self.s = socket.socket()

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
        conn.send(msg)
        conn.close()
        self._loop.selector.unregister(conn)

    def _accept(self, sock):
        conn, addr = sock.accept()
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self._loop.selector.register(conn, selectors.EVENT_READ, self._on_read)

    def run(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(100)
        self.s.setblocking(False)
        self._loop.selector.register(self.s, selectors.EVENT_READ, self._accept)
        self._loop.run_forever()


event_loop = EventLoop()
echo_server = TCPEchoServer('localhost', 8888, event_loop)
echo_server.run()
