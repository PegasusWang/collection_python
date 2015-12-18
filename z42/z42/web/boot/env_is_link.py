#!/usr/bin/env python
# coding:utf-8
import _env
from os.path import abspath, dirname, basename, join, exists, islink
from os import walk, remove, symlink

if __name__ == '__main__':
    FILE = abspath(_env.PREFIX)
    CONFIG = join(FILE, 'z42/web/boot/_env.py')
    for dirpath, dirnames, filenames in walk(FILE):
        if '/.' in dirpath:
            continue
        for filename in filenames:
            if filename != '_env.py':
                continue

            path = join(dirpath, filename)
            if path == CONFIG:
                continue

            if islink(path):
                remove(path)

            txt = """
import sys
from os.path import abspath, dirname, join
PREFIX = abspath(
    join(
        dirname(abspath(__file__)), '%s'
    )
)
if PREFIX not in sys.path:
    sys.path.append(PREFIX)

import z42.web.boot._env
""" % (
                ''.join(['../'] * path[len(FILE) + 1:].count('/')))

            def save():
                print path, FILE
                with open(path, 'w') as infile:
                    infile.write(txt)
            if not exists(path):
                save()
            else:
                with open(path) as readfile:
                    if txt != readfile.read():
                        save()
# print path, 'is not symlink ... ; fixed'
# source = join(''.join(
#    , '_env.py')
# print source
# symlink(source, path)
