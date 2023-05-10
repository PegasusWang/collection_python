#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# 配置日志记录器
logging.basicConfig(filename='example.log', level=logging.DEBUG)

# 记录日志
logging.debug('Debug message')
logging.info('Info message')
logging.warning('Warning message')
logging.error('Error message')
logging.critical('Critical message')
