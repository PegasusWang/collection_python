#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bcrypt

password = 'hahahouhou'

hashed = bcrypt.hashpw(password, bcrypt.gensalt())

if hashed == bcrypt.hashpw(password, hashed):
    print('it matched')
