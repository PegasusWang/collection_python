import selectors
import socket

sel = selectors.DefaultSelector()

DEBUG  = 0
def _print(*args):
    if DEBUG:
        print(*args)


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    _print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        _print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        _print('closing', conn)
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('localhost', 8888))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        print(key, mask)
        callback = key.data
        callback(key.fileobj, mask)
