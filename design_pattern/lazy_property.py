#!/usr/bin/env python
# -*- coding:utf-8 -*-


class lazyproperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val


class T(object):
    def __init__(self, r):
        self.r = r


    @lazyproperty
    def area(self):
        print('copute')
        return 3.14*self.r**2


if __name__ == '__main__':
    c = T(3)
    print(c.r)
    print(c.area)
    print(c.area)
    print(c.area)
    print(c.area)
