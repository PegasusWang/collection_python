#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import schedule
"""
日志记录
"""
logging.basicConfig()
schedule_logger = logging.getLogger('schedule')
# 日志级别为DEBUG
schedule_logger.setLevel(level=logging.DEBUG)


def job():
    print("Hello, Logs")


schedule.every().second.do(job)
schedule.run_all()

schedule.clear()
