#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   simple.py
@Time    :   2023/09/17 20:29:55
@Author  :   jumploop 
@Version :   1.0
@Desc    :   None
'''

import pyinotify

wm = pyinotify.WatchManager()


class EventHandler(pyinotify.ProcessEvent):
    """事件处理"""

    def process_IN_CREATE(self, event):
        """处理文件创建"""
        print("create:", event.pathname)

    def process_IN_DELETE(self, event):
        """处理文件删除"""
        print("delete:", event.pathname)


def main():
    """Program entrance"""
    handler = EventHandler()
    wm.add_watch('/tmp', pyinotify.IN_DELETE | pyinotify.IN_CREATE, rec=True)
    notifier = pyinotify.Notifier(wm, handler)
    notifier.loop()


if __name__ == '__main__':
    main()
