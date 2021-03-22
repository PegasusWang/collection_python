# -*- coding: utf-8 -*-

import socket


s = socket.socket()
s.connect(('localhost', 8888))
while True:
    msg =s.recv(1024)
