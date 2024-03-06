#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from logging import getLogger, StreamHandler, Formatter, DEBUG
from logging.handlers import RotatingFileHandler
from os import makedirs
from os.path import exists, join as path_join, dirname, basename


class Logger:
    """ 封装的用于类的通用功能"""

    def __init__(
            self,
            name="root",
            level=DEBUG,
            filename: str = None,
            max_size: int = 1,
            backup_count: int = 8):
        """
        :param name:            日志名称，默认为root
        :param level:           日志等级，默认为DEBUG
        :param filename:        日志文件名称，默认为该类所在的文件的 文件名.log
        :param max_size:        单个日志文件最大大小，单位 MB，默认为1M
        :param backup_count:    除名称为 filename的文件外, 备份日志的数量
        """
        self.log_handlers_clean()
        self._logger = getLogger(name)
        self._logger.setLevel(level)
        self.level = level
        formatter = Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
        # ======================================================
        log_dir = path_join(dirname(__file__), 'logs')
        # log_dir 目录，如果不存在则创建
        self.__check_dirs(log_dir)
        filename = filename or basename(__file__)
        self.filename = self.__check_log_suffix(filename)
        # log 文件绝对路径
        self.log_file_path = path_join(log_dir, self.filename)
        self.max_size = max_size * 1024 ** 2
        self.backup_count = backup_count
        self.console_handler(formatter)
        self.file_handler(formatter)
        self.log_handlers_clean()

    def file_handler(self, formatter):
        file_handler = RotatingFileHandler(
            filename=self.log_file_path,
            maxBytes=self.max_size,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(self.level)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    def console_handler(self, formatter):
        # log print
        console_handler = StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    @staticmethod
    def __check_dirs(dir_path: str):
        """检查目录是否存在，不存在则递归创建"""
        if not exists(dir_path):
            makedirs(dir_path)

    @staticmethod
    def __check_log_suffix(log_name: str) -> str:
        """确保log_name是以'.log'"""
        suffix = '.log'
        if not log_name.endswith(suffix):
            log_name = f"{log_name}{suffix}"

        return log_name

    @property
    def logger(self):
        return self._logger

    def log_handlers_clean(self):
        """clean logging root log handlers"""
        logging.root.handlers = []
