#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from schedule import every,run_pending,repeat

"""
装饰器安排作业
"""
# 此装饰器效果等同于 schedule.every(10).minutes.do(job)
@repeat(every(10).minutes)
def job():
    print("I am a scheduled job")

while True:
    run_pending()
    time.sleep(1)