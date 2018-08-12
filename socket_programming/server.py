# -*- coding: utf-8 -*-

import socket
import time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


def get(path):
    s = socket.socket()
    s.connect(('localhost', 5000))
    request = 'GET {} HTTP1.0\r\n\r\n'.format(path)

    s.send(request.encode())

    chunks = []
    while True:
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = b''.join(chunks).decode()
            print(body.split('\n')[0])
            return


get('foo')
get('/bar')

selector = DefaultSelector()

def get(path):
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    request = 'GET {} HTTP1.0\r\n\r\n'.format(path)

    selector.register(s.fileno(), EVENT_WRITE)
    selector.select()
    selector.unregister(s.fileno())

    s.send(request.encode())

    chunks = []
    while True:
        selector.register(s.fileno(), EVENT_READ)
        selector.select()
        selector.unregister(s.fileno())
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = b''.join(chunks).decode()
            print(body.split('\n')[0])
            return
