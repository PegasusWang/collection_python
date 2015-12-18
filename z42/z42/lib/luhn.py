#!/usr/bin/env python
#coding:utf-8


def luhn_verify(code):
    code = code.replace(' ', '').strip()
    if not code.isdigit():
        return False
    sum = 0
    for i in xrange(len(code)):
        c = int(code[-i-1])
        if i % 2:
            v = c * 2;
            sum += (v - 9) if (v > 9) else v
        else:
            sum += c
    return sum % 10 == 0

if __name__ == '__main__':
    print luhn_verify('5324505101636252')
    print luhn_verify('532450510163625')

