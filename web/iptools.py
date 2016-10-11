#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import socket


def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


if __name__ == '__main__':
    print(ip2int('10.0.2.2'))
    print(int2ip(ip2int('10.0.2.2')))
