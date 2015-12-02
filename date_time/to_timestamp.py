#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import datetime

def to_timestamp(s):
    format = "%Y-%m-%d %H:%M:%S"
    #format = "%Y-%m-%d"
    ts =time.mktime(datetime.datetime.strptime(s, format).timetuple())
    return int(ts)


def test():
    s = "2015-10-18 00:00:00"
    print to_timestamp(s)

test()
