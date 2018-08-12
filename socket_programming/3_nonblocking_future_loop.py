
# -*- coding: utf-8 -*-
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
