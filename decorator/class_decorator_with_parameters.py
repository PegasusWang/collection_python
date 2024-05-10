#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Decorator:
    def __init__(self, arg1, arg2):
        print('执行类Decorator的__init__()方法')
        self.arg1 = arg1
        self.arg2 = arg2

    def __call__(self, f):
        print('执行类Decorator的__call__()方法')

        def wrap(*args):
            print('执行wrap()')
            print('装饰器参数：', self.arg1, self.arg2)
            print('执行' + f.__name__ + '()')
            f(*args)
            print(f.__name__ + '()执行完毕')

        return wrap


@Decorator('Hello', 'World')
def example(a1, a2, a3):
    print('传入example()的参数：', a1, a2, a3)

if __name__ == '__main__':
    print('装饰完毕')
    print('准备调用example()')
    example('Wish', 'Happy', 'EveryDay')
    print('测试代码执行完毕')