#!/usr/bin/env python
#coding:utf-8
from _gearman import gearman

index = gearman.client('index.index', True)

if __name__ == "__main__":
    print rendermail("/SITE/_mail/sso/root/test.html", 'kzinglzy@gmail.com', 'zfvwg')
