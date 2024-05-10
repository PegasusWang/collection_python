#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

# https://mp.weixin.qq.com/s/G6Jf3zr14ELpNbriY_qvJg

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # 生成事件处理器对象
    event_handle = LoggingEventHandler()
    # 生成监控器对象
    observer = Observer()
    # 注册事件处理器，配置监控目录
    observer.schedule(event_handle, path, recursive=True)
    # 监控器启动-创建线程
    observer.start()
    # 以下代码是为了保持主线程运行
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    # 等待其他的子线程执行结束之后，主线程在终止
    observer.join()
