#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys
import traceback
import time
import datetime
from urlparse import urlparse

def get_date_from_stamp(time_stamp):
    return (
        datetime.datetime.fromtimestamp(
            int(time_stamp)
        ).strftime('%Y-%m-%d %H:%M:%S')
    )

if __name__ == '__main__':
    try:
        timestamp = sys.argv[1]
    except:
        timestamp = time.time()
    print get_date_from_stamp(timestamp)
