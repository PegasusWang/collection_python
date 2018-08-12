#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import datetime

def to_timestamp(s):
    format = "%Y-%m-%d %H:%M:%S"
    #format = "%Y-%m-%d"
    ts =time.mktime(datetime.datetime.strptime(s, format).timetuple())
    return int(ts)


def parse(date_str):
    """parse

    :param date_str: date time string
    :return: datetime obj
    """
    import dateutil
    return dateutil.parser.parse(date_str)


def test():
    s = "2015-10-18 00:00:00"
    print to_timestamp(s)



if __name__ == "__main__":
    #  s = "2017-06-27 00:00:00"
    #  beg = '2017-08-09 11:02:04'
    #  end = '2017-08-11 09:15:00'
    #  print(to_timestamp(beg))
    #  print(to_timestamp(end))
    print(to_timestamp('2017-10-17 17:00:00'))
    print(to_timestamp('2017-10-17 20:00:00'))
