#!/usr/bin/env python
# -*- coding:utf-8 -*-

import grequests

urls = ['http://www.baidu.com'] * 10
rs = (grequests.get(u) for u in urls)

cs = grequests.map(rs)
for i in cs:
    print i.content
