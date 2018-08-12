
# -*- coding: utf-8 -*-

import socket
import time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


selector = DefaultSelector()
num_tasks = 0


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
    selector.register(s.fileno(), EVENT_WRITE, data=callback)   # callback 无法执行到


def connected(s, request):
    selector.unregister(s.fileno())
    # socket 可写
    s.send(request.encode())

    chunks = []

    def callback(): return readable(s, chunks)
    selector.register(s.fileno(), EVENT_READ, data=callback)


def readable(s, chunks):
    global num_tasks
    # s is readable
    selector.unregister(s.fileno())
    chunk = s.recv(1000)
    if chunk:
        chunks.append(chunk)

        def callback(): return readable(s, chunks)
        selector.register(s.fileno(), EVENT_READ, data=callback)
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
        callback = event.data    # 之前注册的 callback
        callback()    # 这里会执行 callback = lambda: connected(s, request)


print(time.time() - start)
