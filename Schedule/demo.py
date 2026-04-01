#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import schedule


def job():
    print("I'm working...")


# 每十分钟执行任务
schedule.every(10).minutes.do(job)
# 每个小时执行任务
schedule.every().hour.do(job)
# 每天的10:30执行任务
schedule.every().day.at("10:30").do(job)
# 每个月执行任务
schedule.every().monday.do(job)
# 每个星期三的13:15分执行任务
schedule.every().wednesday.at("13:15").do(job)
# 每分钟的第17秒执行任务
schedule.every().minute.at(":17").do(job)
# 每10秒执行任务
schedule.every(10).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
