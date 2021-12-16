"""
schedule 是一个定时任务调度库，不用 crontab 也可以实现定时任务了

pip install schedule
https://schedule.readthedocs.io/en/stable/examples.html
"""

import datetime as dt
import os
import time
import schedule


def notify():
    now = dt.datetime.now()
    print('notify:', now)
    title, text = "放音乐啦", "打开控制电源"
    os.system(""" osascript -e 'say "家里放点音乐吧"' """)
    os.system(
        """ osascript -e 'display notification "{}" with title "{}"' """.format(text, title))


schedule.every().day.at("11:13:00").do(notify)
schedule.every().day.at("12:25:00").do(notify)
schedule.every().day.at("13:30:00").do(notify)
schedule.every().day.at("14:15:00").do(notify)
schedule.every().day.at("15:33:00").do(notify)

while True:
    schedule.run_pending()
    time.sleep(1)
