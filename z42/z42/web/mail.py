#!/usr/bin/env python
#coding:utf-8

from smtp import sendmail
from render import render
from z42.config import DEBUG,SMTP

def rendermail(template, to, subject, sender=None, sender_name=None, **kwds):
    html = render(
        template, to=to, sender=sender, sender_name=sender_name, **kwds
    )
    html = html.strip()
    if DEBUG:
        print to
        print subject
        print html
    sendmail(to, subject, None, sender, html, sender_name)

if __name__ == '__main__':
    rendermail('/ANGELCRUNCH/_mail/user/reject.html', '522183104@qq.com', '张沈鹏', reason='test')

