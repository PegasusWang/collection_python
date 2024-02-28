#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import shutil
import os

import psutil
from psutil._common import bytes2human
from loguru import logger


def get_disk_space(path='C:'):
    """
    get disk space
    """
    usage = psutil.disk_usage(path)
    space_total = bytes2human(usage.total)
    space_used = bytes2human(usage.used)
    space_free = bytes2human(usage.free)
    space_used_percent = float(bytes2human(usage.percent)[:-1]) / 100
    logger.info(
        '{0:.2%} : {1}/{2}, remaining capacity {3}',
        space_used_percent, space_used, space_total, space_free
    )
    return space_used_percent


def copy_file():
    """copy file"""
    base_path = r'C:\Users\liming\Downloads\Video'
    to_path = r'E:\新建文件夹'
    file_list = [file for file in os.listdir(base_path) if file.endswith('.mp4')]
    file = file_list.pop()
    old_path = os.path.join(base_path, file)
    new_path = os.path.join(to_path, file)
    try:
        shutil.move(old_path, new_path)
        logger.info(f'copy file {old_path} to {new_path}')
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    while True:
        time.sleep(60)
        space_used_percent = get_disk_space()
        if space_used_percent > 0.7:
            copy_file()
