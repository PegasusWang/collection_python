#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath, dirname, basename, join, exists
from os import walk

FROM_STRING = """
ms_duplex_radio
"""

TO_STRING = """
ms_duplex_checked
"""


def replace(from_string, to_string, suffix):
    from_string = from_string.strip()
    to_string = to_string.strip()
    for from_s, to_s in zip(filter(bool, from_string.split('\n')), filter(bool, to_string.split('\n'))):
        _replace(from_s.strip(), to_s.strip(), suffix)


def _replace(from_string, to_string, suffix=('py', 'htm', 'txt', 'conf', 'css', 'h', 'template', 'js', 'html', 'rst', 'coffee', 'yaml', 'mako', 'sh', 'wsgi')):
    from_string = from_string.strip()
    to_string = to_string.strip()

    file = abspath(__file__)

    for dirpath, dirnames, filenames in walk(dirname(file)):
        dirbase = basename(dirpath)
        if '/.hg/' in dirpath:
            continue
        if dirbase.startswith('.'):
            continue

        for filename in filenames:
            _suffix = filename.rsplit('.', 1)[-1]
            # if suffix not in ('css','html', 'htm', ):
            if _suffix not in suffix:
                continue
            path = join(dirpath, filename)
            if path == file:
                continue
            if not exists(path):
                continue
            with open(path) as f:
                content = f.read()
            t = content.replace(from_string, to_string)
            if t != content:
                with open(path, 'wb') as f:
                    f.write(t)



replace(
    FROM_STRING,
    TO_STRING,
    ('py', 'htm', 'txt', 'conf', 'css', 'h', 'template', 'js', 'html', 'rst', 'coffee')
)
