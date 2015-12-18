#!/usr/bin/env python
#coding:utf-8
from num2code import num_encode, num_decode
from base64 import urlsafe_b64encode as encode, urlsafe_b64decode as decode


def encode_id(id, secret):
    secret = str(secret)
    if not secret.isdigit():
        secret = num_decode(secret)
    id, secret = map(int, (id, secret))
    result = id ^ secret
    return encode(num_encode(result))

def decode_id(encoded, secret):
    encoded_int = num_decode(decode(encoded))
    secret = str(secret)
    if not secret.isdigit():
        secret = num_decode(secret)
    result = encoded_int ^ secret
    return result


if __name__ == '__main__':
    secret = 'safd3f32sf32f'
    f = encode_id(10086, secret)
    print f
    print decode_id(f, secret)

