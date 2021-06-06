#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
import calendar


def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
    return start_date, end_date


def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step


if __name__ == '__main__':
    a_day = timedelta(days=1)
    now = datetime(2012, 4, 5).replace(day=1)
    first_day, last_day = get_month_range(now)
    for d in date_range(first_day, last_day, a_day):
        print(d)
