#!/usr/bin/env python
#coding:utf-8

from hashlib import sha256
from base64 import urlsafe_b64encode

def b64hash(bytes):
    return urlsafe_b64encode(sha256(bytes).digest()).rstrip('=')

