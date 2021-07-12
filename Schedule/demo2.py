#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import schedule

"""
只运行一次任务
"""


def job_that_executes_once():
    print('i\'m working...')
    # 此处编写的任务只会执行一次...
    return schedule.CancelJob


schedule.every().day.at('22:30').do(job_that_executes_once)
while True:
    schedule.run_pending()
    time.sleep(1)
