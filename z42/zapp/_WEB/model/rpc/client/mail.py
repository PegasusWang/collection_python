#!/usr/bin/env python
#coding:utf-8
from _gearman import gearman

rendermail = gearman.client('mail.rendermail', True)

if __name__ == "__main__":
    import mail
    from z42.web.mail import rendermail as _rendermail
    _rendermail("test.html", '375956667@qq.com', 'zfvwg')
    print rendermail("test.html", '375956667@qq.com', 'zfvwg')
