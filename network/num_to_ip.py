#!/usr/bin/env python
# -*- coding: utf-8 -*-
def num_to_ip(num):
    """num to ip converts"""
    parts = [num >> 24 & 0xff, num >> 16 & 0xff, num >> 8 & 0xff, num & 0xff]
    return ".".join(map(str, parts))


def num2ip(num):
    "将十进制整数IP转换成点分十进制的字符串IP地址"
    return ".".join([str(num >> x & 0xff) for x in [24, 16, 8, 0]])


if __name__ == '__main__':
    print(num_to_ip(3232235521))
    print(num2ip(3232235521))
