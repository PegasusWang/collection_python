#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys

if sys.version_info[0] == 2:
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
else:
    pass
