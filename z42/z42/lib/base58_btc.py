#!/usr/bin/env python

"""encode/decode base58 in the same way that Bitcoin does"""

import math
import hashlib

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)


def b58encode(v):
    """ encode v, which is a string of bytes, to base58.            
        """

    long_value = int(v.encode('hex_codec'), 16)

    result = ''
    while long_value >= __b58base:
        div, mod = divmod(long_value, __b58base)
        result = __b58chars[mod] + result
        long_value = div
    result = __b58chars[long_value] + result

    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    nPad = 0
    for c in v:
        if c == '\0': nPad += 1
        else: break

    return (__b58chars[0]*nPad) + result

def b58decode(v, length):
    """ decode v into a string of len bytes
        """

    long_value = 0L
    for (i, c) in enumerate(v[::-1]):
        long_value += __b58chars.find(c) * (__b58base**i)

    result = ''
    while long_value >= 256:
        div, mod = divmod(long_value, 256)
        result = chr(mod) + result
        long_value = div
    result = chr(long_value) + result

    nPad = 0
    for c in v:
        if c == __b58chars[0]: nPad += 1
        else: break

    result = chr(0)*nPad + result
    if length is not None and len(result) != length:
        return None

    return result

def sha_256(data):
    return hashlib.sha256(data).digest()

def checksum(data):
    return sha_256(sha_256(data))

def ripemd_160(data):
    return hashlib.new('ripemd160', data).digest()

def hash_160(public_key):
    h1 = sha_256(public_key)
    h2 = ripemd_160(h1)
    return h2

def public_key_to_btc_address(public_key):
    h160 = hash_160(public_key)
    return hash_160_to_btc_address(h160)

def hash_160_to_btc_address(h160):
    vh160 = '\x00'+h160  # \x00 is version 0
    h3 = sha_256(sha_256(vh160))
    addr = vh160+h3[0:4]
    return b58encode(addr)

def btc_address_to_hash_160(addr):
    bytes = b58decode(addr, 25)
    return bytes[1:21]

def btc_address_verify(address):
    bytes = b58decode(address, 25)
    if bytes:
        ck = checksum(bytes[:-4])[:4]
        #print ord(bytes[0])
        return bytes[-4:] == ck
    return False

if __name__ == '__main__':
    pass
    print btc_verify('1')
    print btc_verify('msTGAm1ApjEJfsWfAaRVaZHRm26mv5GL73')
    print btc_verify('1Q1pE5vPGEEMqRcVRMbtBK842Y6Pzo6nK9')
    print btc_verify('1MsHWS1BnwMc3tLE8G35UXsS58fKipzB7a')

