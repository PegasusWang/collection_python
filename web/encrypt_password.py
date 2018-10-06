#!/usr/bin/env python
# -*- coding:utf-8 -*-

import bcrypt

'''
password = '123456'

hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # encode
print(hashed)

if hashed == bcrypt.hashpw(password.encode('utf-8'), hashed):
    print('it matched')

'''

def gen_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # encode


def check(password, password_hash):
    return password_hash == bcrypt.hashpw(password.encode('utf-8'), password_hash)


def test_check():
    ori_pwd = '1234567'
    input_pwd = '1234567'
    assert check(input_pwd, gen_hash(ori_pwd)) == True



"""
"exemple_remix": {
    "check_member_permission": 0,
    "name": "exemple-remix",
    "key": "ec2b1b",
    "secret": "wCXkKAwqZWlbZ8t0B3Yd"
}
"""
print(gen_hash('exemple-remix'))
