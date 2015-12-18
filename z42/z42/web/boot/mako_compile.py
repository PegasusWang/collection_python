#!/usr/bin/env python
#coding:utf-8
import _env
from zapp.BASE.base.view._render import template_lookup, RENDER_PATH
from os import walk
from os.path import abspath, join
import sys
for path in RENDER_PATH:
    path = abspath(path)
    for (dirpath, dirnames, filenames) in walk(path):
#        if "/BTC/god" in dirpath:
#            continue
        dirpath = abspath(dirpath)[len(path):]
        for filename in filenames:
            if filename.rsplit('.', 1)[-1] in ('swp', 'bak', 'py', 'pyc', '.orig'):
                continue
            filepath = join(dirpath, filename)
            print 'compile', filepath
            try:
                mytemplate = template_lookup.get_template(filepath)
            except:
                import traceback
                traceback.print_exc()

#import sys
#if sys.getdefaultencoding() == 'ascii':
#    reload(sys)
#    sys.setdefaultencoding('utf-8')
#
#
#def main():
#    pass
# 
#if __name__ == "__main__":
#    main()

