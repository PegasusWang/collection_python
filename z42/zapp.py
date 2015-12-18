#!/usr/bin/env python
#coding:utf-8
import _env
from os.path import join, isdir, basename, islink
from os import remove, symlink
from os.path import exists
import glob


LINK_DIR = (
        'coffee' ,
        'static' ,
        'html' ,
        'js' ,
        'css' ,
    )
def zapp_install():
    for i in glob.glob(join(_env.PREFIX, 'zapp/*')):
        if isdir(i):
            name = basename(i)
            for dirpath in LINK_DIR:
                path = join(_env.PREFIX , dirpath, name)
                realpath = join(i, dirpath)
                if islink(path):
                    remove(path)
                realpath = realpath[len(_env.PREFIX)+1:]
                if exists(realpath):
                    symlink('../'+ realpath, path)


def zapp_rm(app):
    for i in LINK_DIR:
        path = join(_env.PREFIX, i, app)
        if islink(path):
            remove(path)

if __name__ == '__main__':
#    zapp_rm("TECH2IPO")
#   zapp_rm('_WEB')
    #zapp_rm('SS0')
    zapp_install()

