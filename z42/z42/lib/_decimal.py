#!/usr/bin/env python
# coding:utf-8

from decimal import *
from decimal import Decimal as _Decimal

PLACE11 = 1/Decimal(10**11)
PLACE8 = _Decimal(10) ** -8
PLACE6 = _Decimal(10) ** -6
PLACE3 = _Decimal(10) ** -3
PLACE2 = Decimal('0.01')

class Decimal(_Decimal):
    def __str__(self):
        if not self:
            return '0'
        s = self.quantize(PLACE8)
        s = '%.8f'%_Decimal(s)
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s

    def quantize(self, exp, rounding=None, context=None, watchexp=True):
        s = super(Decimal, self).quantize(exp, rounding, context, watchexp)
        return Decimal(s)

    def __truediv__(self, other, context=None):
        s = super(Decimal, self).__truediv__(other, context)
        return Decimal(s)

    __div__ = __truediv__

    def __pow__(self, other, modulo=None, context=None):
        s = super(Decimal, self).__pow__(other, modulo, context)
        return Decimal(s)

    def __mul__(self, other, context=None):
        s = super(Decimal, self).__mul__(other, context)
        return Decimal(s)

    def __add__(self, other, context=None):
        s = super(Decimal, self).__add__(other, context)
        return Decimal(s)

    def __sub__(self, other, context=None):
        s = super(Decimal, self).__sub__(other, context)
        return Decimal(s)

if __name__ == '__main__':
    print '%.8f'%Decimal(0001.11)
    print '%.8f'%(Decimal(0.3)/PLACE8)
    print int(round(Decimal(0.3)/PLACE8))
