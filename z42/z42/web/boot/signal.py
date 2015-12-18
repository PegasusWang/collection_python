#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from os.path import abspath, dirname, basename, join, exists
from os import walk
ROOT = join(_env.PREFIX, 'zapp')
prefix = (
    '@signal.'    ,
)
SIGNAL_LIST = []
def pather(path):
    #i = path[len(ROOT)+1:-3].replace("/",".").split(".",2)
    #i[0],i[1]=i[1],i[0]
    #return ".".join(i)
    return "zapp." + path[len(ROOT)+1:-3].replace("/",".")

for dirpath, dirnames, filenames in walk(ROOT):
    if basename(dirpath).startswith('.') or '/z42/web/boot' in dirpath:
        continue

    for filename in filenames:
        if filename.endswith('.py'):
            path = join(dirpath, filename)
            with open(path) as infile:
                for line in infile:
                    push = False
                    line = line.strip()
                    if line.startswith("@signal."):
                        SIGNAL_LIST.append((line.split(".",3)[1], pather(path)))

with open("/".join((_env.PREFIX, "z42/config/_signal.py")),"w") as init:
    init.write("#coding:utf-8\n\n")
    init.write("# 由 42web/z42/web/boot/singal.py 自动生成\n\n")
    init.write("from collections import defaultdict\n")
    init.write("SIGNAL_IMPORT = defaultdict(list)\n")
    for i in SIGNAL_LIST:
        init.write("SIGNAL_IMPORT['%s'].append('%s')"%(i))
        init.write("\n")

