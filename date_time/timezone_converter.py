#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
时区之间互相转化。
http://stackoverflow.com/questions/10997577/python-timezone-conversion
flask可以使用flask_babel插件解决类似国际化等问题
"""

from datetime import datetime
import pytz


"""
localFormat = "%Y-%m-%d %H:%M:%S"
utcmoment_unaware = datetime.utcnow()
utcmoment = utcmoment_unaware.replace(tzinfo=pytz.utc)

# pytz.all_timezones 输出所有时区
timezones = ['America/Los_Angeles', 'Europe/Madrid', 'America/Argentina/San_Juan',
             'Asia/Shanghai']

for tz in timezones:
    localDatetime = utcmoment.astimezone(pytz.timezone(tz))
    print(localDatetime.strftime(localFormat))
"""


def timezone_date(tz='Asia/Shanghai'):
    """ return current date object by timezone
    Args:
        tz (str): one of timezone from pytz.all_timezones
    Returns:
        datetime (datetime.datetime): datetime object
    """
    utcmoment_unaware = datetime.utcnow()
    utcmoment = utcmoment_unaware.replace(tzinfo=pytz.utc)
    local_datetime = utcmoment.astimezone(pytz.timezone(tz))
    return local_datetime


print(timezone_date())
print(timezone_date('America/Recife'))


# 日期字符串和日期对象之间的互相转换

import datetime as dt
from calendar import monthrange
from dateutil import parser


def timestr_to_date_obj(timestr, format_str='%Y-%m-%d'):
    """ 转换date string到date对象
    Returns:
        date (dt.date)
    """
    if isinstance(timestr, dt.date):
        return timestr
    else:
        return dt.datetime.strptime(timestr, format_str).date()


def get_format_datestr(date_str, to_format='%Y-%m-%d'):
    """
    Args:
        date_str (str): ''
        to_format (str): '%Y-%m-%d'

    Returns:
        date string (str)
    """
    date_obj = parser.parse(date_str).date()
    return date_obj.strftime(to_format)


def datestr_to_date(date_str):
    """ 返回date字符串代表的date对象 """
    if isinstance(date_str, dt.date):
        return date_str
    else:
        return parser.parse(date_str).date()


def month_range_date(date_obj):
    """ 根据传入的date返回当月第一天开始和最后一天结束的date """
    # monthrange(2002,1) -> (1, 31)
    start_day, end_day = monthrange(date_obj.year, date_obj.month)
    return (
        dt.date(date_obj.year, date_obj.month, start_day),
        dt.date(date_obj.year, date_obj.month, end_day)
    )
