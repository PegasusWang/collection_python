#!/usr/bin/python
#coding:utf-8
import requests, json

url="http://sendcloud.sohu.com/webapi/mail.send.json"

# 不同于登录SendCloud站点的帐号，您需要登录后台创建发信子帐号，使用子帐号和密码才可以进行邮件的发送。
params = {
    "api_user": "pegasus_test_kTfGDH",
    "api_key" : "aQbHk7BlDJizBwyF",
    "from" : "service@sendcloud.im",
    "fromname" : "网站测试",
    "to" : "291374108@qq.com",
    "subject" : "来自SendCloud的第一封邮件！",
    "html": "欢迎提出改进建议""",
    "resp_email_id": "true",
}

r = requests.post(url, files={}, data=params)
print r.text
