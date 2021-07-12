#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import schedule

"""
标签功能
"""


def greet(name):
    print('Hello {}'.format(name))


# .tag 打标签
schedule.every().day.do(greet, 'Andrea').tag('daily-tasks', 'friend')
schedule.every().hour.do(greet, 'John').tag('hourly-tasks', 'friend')
schedule.every().hour.do(greet, 'Monica').tag('hourly-tasks', 'customer')
schedule.every().day.do(greet, 'Derek').tag('daily-tasks', 'guest')

# get_jobs(标签)：可以获取所有该标签的任务
friends = schedule.get_jobs('friend')

# 取消所有 daily-tasks 标签的任务
schedule.clear('daily-tasks')

while True:
    schedule.run_pending()
    time.sleep(1)
