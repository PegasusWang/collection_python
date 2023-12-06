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


if __name__ == "__main__":
    print(ip_to_num('192.168.0.1'))
