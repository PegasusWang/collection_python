#!/usr/bin/env python
# -*- coding: utf-8 -*-
def ip_to_num(ip):
    """ip to num"""
    parts = list(map(int, ip.split(".")))
    seg0 = parts[0] << 24
    seg1 = parts[1] << 16
    seg2 = parts[2] << 8
    seg3 = parts[3]
    return seg0 | seg1 | seg2 | seg3


def ip2num(ip):
    "将点分十进制IP地址转换成十进制整数"
    items = [int(x) for x in ip.split(".")]
    return sum([items[i] << [24, 16, 8, 0][i] for i in range(4)])


if __name__ == "__main__":
    print(ip_to_num('192.168.0.1'))
    print(ip2num('192.168.0.1'))
