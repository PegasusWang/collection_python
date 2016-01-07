#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bcrypt

password = 'hahahouhou'

hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # encode
print(hashed)

if hashed == bcrypt.hashpw(password.encode('utf-8'), hashed):
    print('it matched')
