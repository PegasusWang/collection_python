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

    def add_writer(self, writer, callback):
        try:
            self._selector.register(writer, selectors.EVENT_WRITE, callback)
        except KeyError:
            pass

    def remove_reader(self, reader):
        try:
            self._selector.unregister(reader)
        except KeyError:
            pass

    def remove_writer(self, writer):
        try:
            self._selector.unregister(writer)
        except KeyError:
            pass

    def register(self, fileobj, mask, data=None):
        self._selector.register(fileobj, mask, data)

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
        loop = self._loop
        self.s.bind((self.host, self.port))
        self.s.listen(100)
        self.s.setblocking(False)
        loop.add_reader(self.s, self._accept)
        loop.run_forever()


loop = EventLoop()
echo_server = TCPEchoServer('localhost', 8888, loop)
echo_server.run()
