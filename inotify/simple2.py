#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyinotify
import os
import pwd
import datetime


class EventHandler(pyinotify.ProcessEvent):
    def process_default(self, event):
        if event.mask & pyinotify.IN_CREATE:
            file_info = os.stat(event.pathname)
            modified_time = datetime.datetime.fromtimestamp(file_info.st_mtime)
            modified_user = pwd.getpwuid(file_info.st_uid).pw_name

            with open("log.txt", "a") as log_file:
                log_file.write("文件/目录创建:\n")
                log_file.write("路径: {0}\n".format(event.pathname))
                log_file.write("创建时间: {0}\n".format(modified_time))
                log_file.write("创建用户: {0}\n\n".format(modified_user))
        if event.mask & pyinotify.IN_MODIFY:
            file_info = os.stat(event.pathname)
            modified_time = datetime.datetime.fromtimestamp(file_info.st_mtime)
            modified_user = pwd.getpwuid(file_info.st_uid).pw_name

            with open("log.txt", "a") as log_file:
                log_file.write("文件/目录修改:\n")
                log_file.write("路径: {0}\n".format(event.pathname))
                log_file.write("修改时间: {0}\n".format(modified_time))
                log_file.write("修改用户: {0}\n\n".format(modified_user))
        elif event.mask & pyinotify.IN_DELETE:
            deleted_time = datetime.datetime.now()
            deleted_user = pwd.getpwuid(os.getuid()).pw_name
            with open("log.txt", "a") as log_file:
                log_file.write("文件/目录删除:\n")
                log_file.write("路径: {0}\n".format(event.pathname))
                log_file.write("修改时间: {0}\n".format(deleted_time))
                log_file.write("修改用户: {0}\n\n".format(deleted_user))


def main():
    """Program entrance"""
    # 创建监控器实例并关联监控器类和目录
    watch_manager = pyinotify.WatchManager()
    event_handler = EventHandler()

    watch_manager.add_watch('/opt/mirrors', pyinotify.ALL_EVENTS, rec=True)
    notifier = pyinotify.Notifier(watch_manager, event_handler)

    # 启动监控器并开始监听目录的变化
    notifier.loop()


if __name__ == '__main__':
    main()
