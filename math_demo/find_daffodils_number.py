#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
寻找水仙花数
说明：
水仙花数也被称为超完全数字不变数、自恋数、自幂数、阿姆斯特朗数，它是一个3位数，
该数字每个位上数字的立方之和正好等于它本身，例如：$1^3 + 5^3+ 3^3=153$。
"""
from __future__ import print_function


def find_daffodils_number():
    """寻找水仙花数"""
    for num in range(100, 1000):
        low = num % 10
        mid = num // 10 % 10
        high = num // 100
        if low**3 + mid**3 + high**3 == num:
            print(f'水仙花数：{num}')


def main():
    """do main"""
    find_daffodils_number()


if __name__ == '__main__':
    main()
