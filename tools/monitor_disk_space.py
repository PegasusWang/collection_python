#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import shutil
import os
import random
import psutil
import glob
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
        space_used_percent,
        space_used,
        space_total,
        space_free,
    )
    return space_used_percent


def copy_file(old_path, new_path):
    """copy file"""
    try:
        logger.info(f'start copy file {old_path} to {new_path}')
        shutil.move(old_path, new_path)
        logger.info(f'copy file {old_path} to {new_path} finished')
    except Exception as e:
        logger.error(e)


def main():
    """Main function"""
    to_path = r'E:\新建文件夹'
    file_list = glob.glob(r'C:\Users\82718\Downloads\Video\*.ts')
    if file_list:
        filepath = random.choice(file_list)
        copy_file(filepath, to_path)
    else:
        logger.warning('Could not find file')


if __name__ == '__main__':
    while True:
        time.sleep(10)
        if get_disk_space() > 0.2:
            main()
