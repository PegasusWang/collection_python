#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from log_handle import logger

from win32com import client as wincom_client

"""
Environment Requirements:
Windows
1. Python 3+
2. Google Chrome
Python Packages
pip install pypiwin32
pip install requests
Folder Structure
--- chrome_helper.py
    file_util.py   


get_file_version() --- 取得版本號
write_json() --- 寫 json file
read_json() --- 讀 json file
"""


def get_file_version(file_path):
    logger.info('Get file version of [%s]', file_path)
    if not os.path.isfile(file_path):
        logger.error('{!r} is not found.'.format(file_path))
        raise FileNotFoundError('{!r} is not found.'.format(file_path))

    wincom_obj = wincom_client.Dispatch('Scripting.FileSystemObject')
    version = wincom_obj.GetFileVersion(file_path)
    logger.info('The file version of [%s] is %s', file_path, version)
    return version.strip()


def write_json(file_path, data):
    with  open(file_path, 'w', encoding='utf-8')as f:
        json.dump(data, f, indent=2)


def read_json(file_path):
    with open(file_path, encoding='utf-8')as f:
        data = json.load(f)
    return data
