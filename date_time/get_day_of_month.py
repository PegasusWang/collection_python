#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
var year = 2015
var month = 9
var date = new Date(year, month-1);    /* js month begin with 0 */
var date_first = new Date(date.getFullYear(), date.getMonth(), 1);
var date_last = new Date(date.getFullYear(), date.getMonth() + 1, 0);
'''

import datetime
"""得到月份的第一天和最后一天"""
year = 2015
month = 4
#date_first = datetime.datetime(datetime.date.today().year,datetime.date.today().month,1)
#date_last = datetime.datetime(datetime.date.today().year,datetime.date.today().month+1,1)-datetime.timedelta(1)

date_first = datetime.datetime(year , month, 1)
date_last = datetime.datetime(year, month+1, 1) - datetime.timedelta(1)

print date_first
print date_last
