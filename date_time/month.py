#!/usr/bin/env python
# -*- coding:utf-8 -*-


from datetime import datetime, timedelta


def diff_month(st_year, st_month, end_year, end_month):
    """计算月分差"""
    d1 = datetime(year=st_year, month=st_month, day=1)
    d2 = datetime(year=end_year, month=end_month, day=1)
    return abs((d1.year - d2.year) * 12 + d1.month - d2.month)


def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m + 1


def _month_year_iter(start_year, start_month, end_year, end_month):
    """ iter month year

    >>> list(_month_year_iter(2014,12,2015,2))
    [(2014, 12), (2015, 1)]
    """
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m + 1


def main():
    st_year = 2015
    st_month = 1
    data = [1, 2, 3, 4]
    beg = (diff_month(st_year, st_month, 2015, 1))
    end = (diff_month(st_year, st_month, 2015, 7))
    print(data[beg:end])


def test():
    for year, month in _month_year_iter(2014, 8, 2015, 7):
        print(year, month)


if __name__ == '__main__':
    test()
    import doctest
    # doctest.testmod()
