#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   watchd.py
@Time    :   2023/09/17 19:16:14
@Author  :   jumploop 
@Version :   1.0
@Desc    :   None
'''

import datetime
import time

from watchdog.events import *
from watchdog.observers import Observer


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


class FileEventHandler(FileSystemEventHandler):
    """file event handler"""

    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            logger.info(
                "directory moved from %s to %s", event.src_path, event.dest_path
            )
        else:
            logger.info("file moved from %s to %s", event.src_path, event.dest_path)

    def on_created(self, event):
        if event.is_directory:
            logger.info("directory created:%s", event.src_path)
        else:
            logger.info("file created:%s", event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            logger.info("directory deleted:%s", event.src_path)
        else:
            logger.info("file deleted:%s", event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            logger.info("directory modified:%s", event.src_path)
        else:
            logger.info("file modified:%s", event.src_path)


if __name__ == "__main__":
    logger = Logger().statup("test.log", stream=True)
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, "/opt", True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
