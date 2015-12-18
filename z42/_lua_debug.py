#!/usr/bin/env python
#coding:utf-8


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
from zapp.BTC.model._redis import redis

while True:
    print redis.brpop('DEBUG')[1]
