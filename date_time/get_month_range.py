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


if __name__ == '__main__':
    a_day = timedelta(days=1)
    now = datetime(2012, 4, 5).replace(day=1)
    first_day, last_day = get_month_range(now)
    while first_day < last_day:
        print(first_day)
        first_day += a_day
