#!/usr/bin/env python
#coding:utf-8
import _redis
from redis.client import Script
help(Script)

if __name__ == '__main__':
    import sys
    if sys.getdefaultencoding() == 'ascii':
        reload(sys)
        sys.setdefaultencoding('utf-8')





