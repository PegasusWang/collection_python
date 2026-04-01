#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 发件人邮箱
asender = "PyDataAnalysis@163.com"
# 收件人邮箱
areceiver = "PyDataAnalysis@163.com"
# 抄送人邮箱
acc = "数据分析@163.com"
# 邮箱主题
asubject = "谢谢关注"
# 发件人地址
from_addr = "PyDataAnalysis@163.com"
# 邮箱授权码
password = "####"
# 邮件设置
msg = MIMEMultipart()
msg['Subject'] = asubject
msg['to'] = areceiver
msg['Cc'] = acc
msg['from'] = "数据分析"
# 邮件正文
body = "你好，欢迎关注@公众号：数据分析，您的关注就是我继续创作的动力！"
msg.attach(MIMEText(body, 'plain', 'utf-8'))
# 添加附件
htmlFile = 'C:/Users/10799/problem.html'
html = MIMEApplication(open(htmlFile, 'rb').read())
html.add_header('Content-Disposition', 'attachment', filename='html')

msg.attach(html)
# 设置邮箱服务器地址和接口
smtp_server = "smtp.163.com"
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
# 登录邮箱
server.login(from_addr, password)
# 发生邮箱
server.sendmail(from_addr, areceiver.split(',') + acc.split(','), msg.as_string())
# 断开服务器连接
server.quit()
