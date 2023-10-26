# -*- coding: utf-8 -*-

"""
schedule 是一个定时任务调度库，不用 crontab 也可以实现定时任务了，支持更加灵活的定时或者一次性任务

pip install schedule

https://schedule.readthedocs.io/en/stable/examples.html
"""

import datetime as dt
import os
import time
import schedule
import logging


def notify():
    try:
        now = dt.datetime.now()
        print('notify:', now)
        title, text = "放音乐啦", "打开控制电源"
        os.system(""" osascript -e 'say "家里放点音乐吧"' """)
        os.system(
            """ osascript -e 'display notification "{}" with title "{}"' """.format(text, title))
    except Exception as e: # 这里包一层 try/catch 防止定时函数因为异常整个进程退出了
        logging.exception(e)


schedule.every().day.at("11:13:00").do(notify)
schedule.every().day.at("12:25:00").do(notify)
schedule.every().day.at("13:30:00").do(notify)
schedule.every().day.at("14:15:00").do(notify)
schedule.every().day.at("15:33:00").do(notify)

while True:
    schedule.run_pending()
    time.sleep(1)  # 防止 cpu 占用太高。https://github.com/dbader/schedule/issues/209
