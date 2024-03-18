#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/27 17:59
# @Author  : 一叶知秋
# @File    : make_tar_file.py
# @Software: PyCharm
from __future__ import division, print_function
import os
import sys
import tarfile
import logging

if sys.version_info[0] == 2:
    input = raw_input
else:
    input = input
formatter = '%(asctime)s %(levelname)s %(filename)s[%(lineno)d]: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=formatter,
                    datefmt='%Y:%m:%d %H:%M:%S', encoding='utf-8')


def make_tar_file(filename, filepath):
    """
    make tar file
    :param filename: tar file name
    :param filepath: source file directory
    :return:
    """
    with tarfile.open(filename, mode='w:gz') as tar:
        for root, dirs, files in os.walk(filepath):
            for file in files:
                fullpath = os.path.join(root, file)
                logging.info('file name: %s', fullpath)
                arcname = fullpath.replace(filepath, '')
                tar.add(fullpath, arcname)


def main():
    """do main"""
    sourceFolder = input('请输入源文件路径目录：\n')
    filename = input('请输入压缩文件名字： \n')
    logging.info('source file dir: %s', sourceFolder)
    logging.info('file name: %s', filename)
    make_tar_file(filename, sourceFolder)


if __name__ == '__main__':
    main()
