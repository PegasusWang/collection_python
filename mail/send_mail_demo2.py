#!/usr/bin/env python
# -*- coding: utf-8 -*-
# smtplib模块主要负责发送邮件：是一个发送邮件的动作，连接邮箱服务器，登录邮箱，发送邮件（有发件人，收信人，邮件内容）。
import smtplib
# email模块主要负责构造邮件：指的是邮箱页面显示的一些构造，如发件人，收件人，主题，正文，附件等
from email.mime.text import MIMEText
from email.header import Header

import openpyxl

"""
需要安装 openpyxl库

pip install openpyxl
"""
# =============================
# 定义变量
# =============================
# 第三方 SMTP 服务

mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "172212595@qq.com"  # 用户名
mail_pass = "*******"  # 授权码 qq邮箱获取地址：https://jingyan.baidu.com/article/6079ad0eb14aaa28fe86db5a.html

sender = '172212595@qq.com'  # 发送邮件的邮箱
to_addrs = ['172212595@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# =============================
# 配置邮件内容；参考：https://www.cnblogs.com/yufeihlf/p/5726619.html
# =============================
mail_msg = """
<p>Python 邮件发送测试,此处是正文...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>
"""
message = MIMEText(mail_msg, 'html', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')  # 发送者
message['To'] = Header("测试", 'utf-8')  # 接收者

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')


def send_mail():
    # =============================
    # 发送邮件配置
    # =============================
    try:
        smtpObj = smtplib.SMTP()  # 实例化SMTP()
        smtpObj.connect(mail_host, 25)  # mail_host 设置服务器；25 为 SMTP 默认端口号
        smtpObj.login(mail_user, mail_pass)  # mail_user 发件人用户名；mail_pass 发件人邮箱授权码
        smtpObj.sendmail(sender, to_addrs,
                         message.as_string())  # sender 发件人邮箱；to_addrs 邮件接收者地址。多个采用字符串列表['接收地址1','接收地址2','接收地址3',...]单个：'接收地址' ； message 发送的内容
        smtpObj.quit()  # 用于结束SMTP会话。
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

if __name__ == '__main__':
    send_mail()