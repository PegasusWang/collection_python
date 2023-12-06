#!/usr/bin/env python
# -*- coding: utf-8 -*-
def num_to_ip(num):
    """num to ip converts"""
    parts = [num >> 24 & 0xff, num >> 16 & 0xff, num >> 8 & 0xff, num & 0xff]
    return ".".join(map(str, parts))


if __name__ == '__main__':
    print(num_to_ip(3232235521))

