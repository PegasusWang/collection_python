#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import schedule

"""
获取目前所有的作业
取消所有作业
"""

def greet(name):
    print('Hello', name)


def hello():
    print('Hello world')


# do() 将额外的参数传递给job函数
schedule.every(2).seconds.do(greet, 'Alice')
schedule.every(4).seconds.do(greet, 'Bob')
schedule.every(6).seconds.do(greet, name='jack')

schedule.every().second.do(hello)
# 获取目前所有的作业
all_jobs = schedule.get_jobs()
print(all_jobs)
# 取消所有作业
schedule.clear()

while True:
    schedule.run_pending()
    time.sleep(1)
