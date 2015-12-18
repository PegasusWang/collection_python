#!/usr/bin/env python
# coding:utf-8
import _env
from os import urandom
from zapp._WEB.model._db import redis, Doc
from hashlib import sha512
from bson.binary import Binary


class Password(Doc):
    structure = dict(
        id=int,
        salt_hash=Binary,
    )
    indexes = [
        {'fields':['id']}
    ]

    
def password_hash_new(password):
    salt = urandom(64)
    hash = sha512(salt + str(password)).digest()
    return salt + hash


def password_hash_verify(password, hash):
    salt = hash[:64]
    return sha512(salt + str(password)).digest() == hash[64:]

def password_verify(user_id, password):
    o = Password.find_one(dict(id=int(user_id)))
    if o:
        return password_hash_verify(password, o.salt_hash)

def password_new(user_id, password):
    Password(dict(
        salt_hash = Binary(password_hash_new(password))
    )).upsert(dict(id=int(user_id)))

if __name__ == "__main__":
    password = "112345"
    print password_hash_new(11)
   
