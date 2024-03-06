#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logger import Logger


logger = Logger().logger

logger.info('hello world')
logger.warning('warning')
logger.error("error")
logger.critical('critical')
