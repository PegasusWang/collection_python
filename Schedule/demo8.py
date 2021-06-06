#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
import schedule
"""
并行执行

默认情况下，Schedule 按顺序执行所有作业。其背后的原因是，很难找到让每个人都高兴的并行执行模型。

不过你可以通过多线程的形式来运行每个作业以解决此限制：
"""
def job1():
    print("I'm running on threads %s" % threading.current_thread())
def job2():
    print("I'm running on threads %s" % threading.current_thread())
def job3():
    print("I'm running on threads %s" % threading.current_thread())

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(10).seconds.do(run_threaded, job1)
schedule.every(10).seconds.do(run_threaded, job2)
schedule.every(10).seconds.do(run_threaded, job3)

while True:
    schedule.run_pending()
    time.sleep(1)
