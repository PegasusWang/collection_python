#!/usr/bin/env python
# -*- coding:utf-8 -*-


import datetime
import sys
import time


def datetime_from_timestamp(time_stamp):
    try:
        return datetime.datetime.fromtimestamp(int(time_stamp))
    except ValueError:
        return datetime.datetime.fromtimestamp(int(time_stamp/1000.0))


def datestr_from_stamp(time_stamp):
    try:
        return (
            datetime.datetime.fromtimestamp(
                int(time_stamp)
            ).strftime('%Y-%m-%d %H:%M:%S')
        )
    except ValueError:
        return (
            datetime.datetime.fromtimestamp(
                int(time_stamp/1000.0)
            ).strftime('%Y-%m-%d %H:%M:%S')
        )


def get_year_from_stamp(time_stamp):
    return (
        datetime.datetime.fromtimestamp(
            int(time_stamp)
        ).strftime('%Y_%m')
    )


def timestamp_by_year_month(year, month):
    """根据时间戳生成该年月第一天的时间戳"""
    d =  datetime.datetime(year=int(year), month=int(month), day=1)
    epoch = datetime.datetime(1970, 1, 1)
    td = d - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6


def test():
    time_stamp = time.time()
    d = datetime.datetime.fromtimestamp(int(time_stamp))
    return d.year, d.month


def days_from_now(timestamp):
    """计算给定时间戳距离现在有多少天"""
    now = datetime.datetime.now()
    s = 1456415452
    print(datestr_from_stamp(s))
    date = datetime_from_timestamp(s)
    print(now-date).days


def main():
    try:
        timestamp = sys.argv[1]
    except:
        timestamp = time.time()
    print(datetime_from_timestamp(timestamp))


if __name__ == '__main__':
    main()
