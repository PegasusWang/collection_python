#!/usr/bin/env python
#coding:utf-8

#!/usr/bin/env python
# coding:utf-8
from baseconv import BaseConverter
import string
import random


class IdEncoder(object):
    _base26 = BaseConverter('1#$MYBKRAVJNLGT95C6S4DU8PXQHIW3E2F7Z')
    _base26r = BaseConverter('5GBHX$Z3A1MEQCT#NSYKIR48U7FJ692VPDWL')

    @classmethod
    def encode(cls, n):
        return cls._base26.encode(n)+cls._base26r.encode(n)

    @classmethod
    def decode(cls, n):
        n = n.upper()
        m = len(n)/2
        try:
            id1 = cls._base26.decode(n[:m])
        except (IndexError, ValueError):
            return
        try:
            id2 = cls._base26r.decode(n[m:])
        except (IndexError, ValueError):
            return
        if id1 == id2:
            return id1


if __name__ == '__main__':
    a = 1074
    b = IdEncoder.encode(a)
    print b
    print IdEncoder.decode(b)
    print a
    print IdEncoder.decode('在我区')
    print IdEncoder.decode('RHI3J7')
