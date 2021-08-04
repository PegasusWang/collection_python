#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import yagmail
from imbox import Imbox
from PIL import ImageGrab
"""
需要安装的包
pip install imbox
pip install yagmail
pip install pillow
pip install keyring

"""

def send_mail(sender, to, contents):
    smtp = yagmail.SMTP(user=sender, host='smtp.qq.com')
    smtp.send(to, subject='Remote Control', contents=contents)


def read_mail(username, password):
    with Imbox('imap.qq.com', username, password, ssl=True) as box:
        all_msg = box.messages(unread=True)
        for uid, message in all_msg:
            # 如果是手机端发来的远程控制邮件
            if message.subject == 'Remote Control':
                # 标记为已读
                box.mark_seen(uid)
                return message.body['plain'][0]


def shutdown():
    os.system('shutdown -s -t 0')


def grab(sender, to):
    surface = ImageGrab.grab()
    surface.save('surface.jpg')
    send_mail(sender, to, ['surface.jpg'])


def main():
    username = '982698078@qq.com'
    password = '你的邮箱授权码'
    receiver = 'xxxxx@qq.com'
    time_space = 5
    yagmail.register(username, password)
    while True:
        # 读取未读邮件
        msg = read_mail(username, password)
        if msg:
            if msg == 'shutdown':
                shutdown()
            elif msg == 'grab':
                grab(username, receiver)
        time.sleep(time_space)


if __name__ == '__main__':
    main()
