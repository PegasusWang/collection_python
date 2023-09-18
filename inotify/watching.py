#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   watching.py
@Time    :   2023/09/17 17:34:17
@Author  :   jumploop 
@Version :   1.0
@Desc    :   None
'''

import os
import pwd
import shutil
import time
import datetime
import logging
import logging.handlers
from concurrent.futures import ThreadPoolExecutor

import pyinotify


def copy_files(path):
    """copy file"""
    logger.info('copy file %s starting', path)
    shutil.copy(path, "/tmp")
    logger.info('copy file %s finished', path)


class Logger:
    """log record"""

    def __init__(self):
        self.logger = logging.getLogger('watching')
        self.logger.setLevel(logging.INFO)

    def statup(self, path, stream=True):
        """statup"""
        write_handler = logging.handlers.TimedRotatingFileHandler(
            path,
            when='midnight',
            interval=1,
            backupCount=7,
            atTime=datetime.time(0, 0, 0, 0),
        )
        write_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(module)s[:%(lineno)d] - %(message)s"
            )
        )

        if stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(module)s[:%(lineno)d] - %(message)s"
                )
            )
            self.logger.addHandler(stream_handler)
        self.logger.addHandler(write_handler)

        return self.logger


class MonitorEvent(pyinotify.ProcessEvent):
    """monitor event"""

    def __init__(self, func):
        super().__init__()
        self.func = func
        self.flag = time.time()

    def process_IN_CREATE(self, event):
        """
        文件被创建
        """
        if time.time() - self.flag > 0:
            logger.info("%s 被创建！", event.pathname)
            self.flag = time.time()
            # 这里就可以做想做的事情了

    def process_IN_MODIFY(self, event):
        """文件被修改"""
        if time.time() - self.flag > 3:
            file_info = os.stat(event.pathname)
            modified_time = datetime.datetime.fromtimestamp(file_info.st_mtime)
            modified_user = pwd.getpwuid(file_info.st_uid).pw_name
            logger.info(
                "文件/目录修改:\n路径:%s, 修改时间: %s, 修改用户:%s",
                event.pathname,
                modified_time,
                modified_user,
            )
            self.flag = time.time()
            # 这里就可以做想做的事情了
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.submit(self.func, event.pathname)

    def process_IN_DELETE(self, event):
        """文件被删除"""
        if time.time() - self.flag > 0:
            logger.info("%s 被删除！", event.pathname)
            self.flag = time.time()
            # 这里就可以做想做的事情了
            deleted_time = datetime.datetime.now()
            deleted_user = pwd.getpwuid(os.getuid()).pw_name
            logger.info(
                "文件/目录删除:\n路径:%s, 修改时间: %s, 修改用户:%s",
                event.pathname,
                deleted_time,
                deleted_user,
            )

    def process_IN_CLOSE_WRITE(self, event):
        """文件写入完毕"""
        if time.time() - self.flag > 0:
            logger.info("%s 写入完毕！", event.pathname)
            self.flag = time.time()
            # 这里就可以做想做的事情了


def main():
    """main function"""
    path = '/opt'  # 监控目录
    watch_manager = pyinotify.WatchManager()
    watch_manager.add_watch(path, pyinotify.ALL_EVENTS, rec=True)
    event = MonitorEvent(func=copy_files)
    notifier = pyinotify.ThreadedNotifier(watch_manager, event)
    notifier.loop()


if __name__ == '__main__':
    logger = Logger().statup("test.log", stream=True)
    main()
