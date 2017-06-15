#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""用来生成tornado的cookie secret"""


import uuid
import base64


print(base64.b64encode(uuid.uuid4().bytes+uuid.uuid4().bytes))


def random_password(length=10):
    import M2Crypto
    import string
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    password = ''
    for i in range(length):
        password += chars[ord(M2Crypto.m2.rand_bytes(1)) % len(chars)]
    return password
