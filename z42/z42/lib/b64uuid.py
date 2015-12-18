#!/usr/bin/env python
#coding:utf-8
from uuid import uuid4
from base64 import urlsafe_b64encode

def b64uuid():
    return urlsafe_b64encode(uuid4().bytes).rstrip('=')

if __name__ == '__main__':
    print b64uuid()

