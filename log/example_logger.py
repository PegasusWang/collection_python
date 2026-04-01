#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# 创建一个日志记录器
logger = logging.getLogger('example_logger')
logger.setLevel(logging.DEBUG)

# 创建一个日志处理程序，将日志输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 创建一个日志处理程序，将日志输出到文件
file_handler = logging.FileHandler('example.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 记录一些日志
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
