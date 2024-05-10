#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/5 15:58
# @Author  : 一叶知秋
# @File    : fib.py
# @Software: PyCharm
class Fib:
    def __init__(self, num):
        self.num = num
        self.a, self.b = 0, 1
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx < self.num:
            self.a, self.b = self.b, self.a + self.b
            self.idx += 1
            return self.a
        raise StopIteration()


def fib(num):
    a, b = 0, 1
    idx = 0
    while idx < num:
        a, b = b, a + b
        idx += 1
        yield a


def fib2(num):
    a, b = 0, 1
    for _ in range(num):
        a, b = b, a + b
        yield a


if __name__ == '__main__':
    f = Fib(10)
    print(list(f))
    print(list(fib(10)))
    print(list(fib2(10)))
