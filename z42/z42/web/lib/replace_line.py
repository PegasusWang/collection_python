#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath, dirname, basename, join, exists, join, dirname, isdir, abspath
from os import walk
import os.path

def link_path(l):
    """
    Return an absolute path for the destination 
    of a symlink
    """
    if os.path.islink(l):
        p = os.readlink(l)
        if os.path.isabs(p):
            return p
        l = os.path.join(os.path.dirname(l), p)
    return abspath(l)


EXIST = set()
def replace(path, suffix_list=('py', 'htm', 'txt', 'conf', 'css', 'h', 'template', 'js', 'html', 'rst', 'coffee')):
    if type(suffix_list) == str:
        suffix_list = [suffix_list]
    for dirpath, dirnames, filenames in walk(abspath(path)):
        for dirname in dirnames:
            path = join(dirpath, dirname)
            if os.path.islink(path):
                path_new = link_path(path)
                if path_new not in EXIST and isdir(path_new):
                    EXIST.add(path_new)
                    for i in replace(path_new, suffix_list):
                        yield i
        #print path_new not in EXIST, isdir(path_new), path_new

        dirbase = basename(dirpath)
        if dirbase.startswith('.'):
            continue

        for filename in filenames:
            path = join(dirpath, filename)

            suffix = filename.rsplit('.', 1)[-1]
            #print filename, suffix
            #if suffix not in ('css','html', 'htm', ):
            if suffix not in suffix_list:
                continue
            if path == file:
                continue
            if not exists(path):
                continue
            with open(path) as f:
                yield path, f


