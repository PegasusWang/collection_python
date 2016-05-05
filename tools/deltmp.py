#!/usr/bin/env python
# -*- coding: utf-8 -*-


DEL_LIST = [
    r"npm-debug\.log",
    r'.*\.pyc$',
    r'.*\.bak$',
    r'.*\.swp$',
    r'^__pycache__$',
    r'.*\.orig$',
    r'^core\.\d+$',
    r'^nohup\.out$',
    r'^:w$',
]

from os.path import join
import os
from os import getcwd, walk, rmdir, chmod
import re
import stat


def write_able(name):
    path = join(root, name)
    chmod(path, stat.S_IWRITE)
    return path

remove = lambda name: os.remove(write_able(name))


def del_dir(dir):
    for root, dirs, files in walk(dir, topdown=False):

        for name in files:
            remove(name)
        for name in dirs:
            rmdir(write_able(name))
    rmdir(dir)

DEL_LIST = [re.compile(i) for i in DEL_LIST]

for root, dirs, files in walk(getcwd(), topdown=False):
    for i in DEL_LIST:
        j = ''

        def if_match(func):
            if i.match(j):
                func(join(root, j))
                print join(root, j)

        for j in dirs:
            if_match(del_dir)

        for j in files:
            if_match(remove)
