# -*- coding: utf-8 -*-

import socket
import select
import sys


class Connection:
    def __init__(self):
        self.s = socket.socket()
        self.s.connect(('localhost', 8888))

    def fileno(self):
        return self.s.fileno()

    def on_read(self):
        msg = self.s.recv(1024).decode('utf8')
        print(msg)

    def send(self, msg):
        self.s.send(msg)


class Input:
    def __init__(self, sender):
        self.sender = sender

    def fileno(self):
        return sys.stdin.fileno()

    def on_read(self):
        msg = sys.stdin.readline().encode('utf8')
        self.sender.send(msg)


s = Connection()
input_reader = Input(s)


class EventLoop:
    def __init__(self):
        self.readers = []

    def add_reader(self, reader):
        self.readers.append(reader)

    def run_forever(self):
        while True:
            readers, _, _ = select.select(self.readers, [], [])
            for reader in readers:
                reader.on_read()


event_loop = EventLoop()
event_loop.add_reader(s)
event_loop.add_reader(input_reader)
event_loop.run_forever()
