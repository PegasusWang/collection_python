# -*- coding: utf-8 -*-

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
