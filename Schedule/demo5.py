#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
import schedule

"""
设定作业截止时间
"""


def job():
    print('Boo')


# 每个小时运行作业，18:30后停止
schedule.every(1).hours.until('18:30').do(job)

# 每个小时运行作业，2030-01-01 18:33 today
schedule.every(1).hours.until('2030-01-01 18:33').do(job)

# 每个小时运行作业，8个小时后停止
schedule.every(1).hours.until(timedelta(hours=8)).do(job)

# 每个小时运行作业，11:32:42后停止
schedule.every(1).hours.until(time(11,32,42)).do(job)

# 每个小时运行作业，2020-5-17 11:36:20后停止
schedule.every(1).hours.until(datetime(2020, 5, 17, 11, 36, 20)).do(job)

# 截止日期之后，该作业将无法运行。
while True:
    schedule.run_pending()
