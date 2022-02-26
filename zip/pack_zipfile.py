#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/26 16:55
# @Author  : 一叶知秋
# @File    : pack_zipfile.py
# @Software: PyCharm
from __future__ import print_function
import os
import sys
import zipfile
import logging

if sys.version_info[0] == 2:
    input = raw_input
else:
    input = input
formatter = '%(asctime)s %(levelname)s %(filename)s[%(lineno)d]: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=formatter,
                    datefmt='%Y:%m:%d %H:%M:%S', encoding='utf-8')


def make_zip_file(filename, sourcefolder):
    """
    make zip file
    :param filename: zip file name
    :param sourceFolder: source file folder
    :return:
    """
    with zipfile.ZipFile(filename, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(sourcefolder):
            for file in files:
                fullpath = os.path.join(root, file)
                logging.info('filename is %s', fullpath)
                arcname = fullpath.replace(sourcefolder, '')
                logging.info('arcname is %s', arcname)
                zip_file.write(fullpath, arcname)


def main():
    sourceFolder = input('请输入源文件路径目录：\n')
    filename = input('请输入压缩文件名字： \n')
    logging.info('source file dir: %s', sourceFolder)
    logging.info('zip file name: %s', filename)
    make_zip_file(filename, sourceFolder)


if __name__ == '__main__':
    main()
