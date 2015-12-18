#!/usr/bin/env python
# -*- coding: utf-8 -*-

def attrcache(f):
    name = f.__name__
    @property
    def _attrcache(self):
        d = self.__dict__
        if name in d:
            return d[name]
        result = f(self)
        d[name] = result
        return result

    return _attrcache

if __name__ == '__main__':

    def x():
        print 'call x()'
        return 12

    class Xxx(object):
        b = 1
        @attrcache
        def x(self):
            print 'call Xxx.x()'
            return x()

        @x.setter
        def x(self , value):
            self._x = value
    class Xxx1(object):
        def x(self):
            print 'call Xxx1.x()'
            return x()


    print Xxx.__dict__
    xxx = Xxx()
    print xxx.__dict__
    print 'xxx.x', xxx.x
    print xxx.__dict__
    print 'xxx.x', xxx.x
    print 'xxx.x', xxx.x
    xxx.x = 222
    print xxx.__dict__
    print '-------------------------------------'
    xxx1 = Xxx1()
    print 'xxx1.x', xxx1.x()
    print 'xxx1.x', xxx1.x()
    print 'xxx1.x', xxx1.x()
