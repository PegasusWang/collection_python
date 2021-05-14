#!/usr/bin/env python
# -*- coding: utf-8 -*-
import schedule

"""
立即运行所有作业，而不管其安排如何
"""


def job_1():
    print('Foo')


def job_2():
    print('Bar')


schedule.every().monday.at("12:40").do(job_1)
schedule.every().tuesday.at("16:40").do(job_2)

schedule.run_all()
# 立即运行所有作业，每次作业间隔10秒
schedule.run_all(delay_seconds=10)
