
#coding:utf-8

import os
from threading import Timer
import socket
import sys
import requests
from datetime import datetime

def sendmail(to, subject, html):
    url = 'https://sendcloud.sohu.com/webapi/mail.send.xml'

    params = {
        'api_user': 'postmaster@42.sendcloud.org',
        'api_key' : 'kMCzqBPv',
        'to' : to,
        'from' : 'alert@42.sendcloud.org',
        'fromname' : '42btc',
        'subject' :  subject,
        'html': html
    }

    r = requests.post(url, data=params)
    if r.text.find('error') != -1:
        return r.text




class Heartbeat(object):
    def __init__(self, interval=60):
        self._quit = None
        self._interval = interval

    def quit(self, func):
        self._quit = func
        return func

    def _sendmail(self):
        title = '%s : %s %s'%(
            socket.gethostname(),
            ' '.join(sys.argv),
            datetime.now(),
        )
        html = """
%s 
"""%title
        #sendmail('42btc-alert@googlegroups.com', '进程自杀 : %s' % title, html)

    def is_alive(self, func):
        def _():
            if not func():
                if self._quit is not None:
                    self._quit()
                self._sendmail()
                os.kill(os.getpid(), 9)
            else:
                Timer(self._interval, _).start()
        Timer(self._interval+60, _).start()
        return _

heartbeat = Heartbeat(5)

