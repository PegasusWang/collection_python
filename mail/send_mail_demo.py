#!/usr/bin/env python
# -*- coding:utf-8 -*-


from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from config import MailConfig

"""
注意需要邮箱pop3开启，设置独立密码，下边的password也是独立密码，
非登录密码
"""

send_to_mail_list = ['291374108@qq.com']


mailInfo = {
    "from": MailConfig.USERNAME,
    "to": ', '.join(send_to_mail_list),
    "hostname": MailConfig.HOSTNAME,
    "username": MailConfig.USERNAME,
    "password": MailConfig.PASSWORD,    # 邮箱独立密码，非登录密码
    "mailsubject": "我是标题",
    "mailtext": "使用python脚本发的测试邮件。",
    "mailencoding": "utf-8",
    "mailtype": "plain",
}


def send_mail():
    smtp = SMTP_SSL(mailInfo["hostname"])
    smtp.set_debuglevel(1)
    smtp.ehlo(mailInfo["hostname"])
    smtp.login(mailInfo["username"], mailInfo["password"])

    msg = MIMEText(mailInfo["mailtext"], mailInfo["mailtype"],
                   mailInfo["mailencoding"])
    msg["Subject"] = Header(mailInfo["mailsubject"], mailInfo["mailencoding"])
    msg["from"] = mailInfo["from"]
    msg["to"] = mailInfo["to"]
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    smtp.sendmail(mailInfo["from"], mailInfo["to"], msg.as_string())

    smtp.quit()

if __name__ == '__main__':
    send_mail()
