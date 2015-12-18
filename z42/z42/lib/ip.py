#!/usr/bin/env python
#coding:utf-8
import socket, fcntl, struct

def get_local_ip(ifname='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret

if __name__ == '__main__':
    print get_local_ip()
