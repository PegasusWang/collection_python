#!/usr/bin/env python
# -*- coding:utf-8 -*-



debug_s = """__import__('traceback').print_exc();__import__('pprint').pprint(locals())"""
if __name__ == '__main__':
    try:
        raise Exception()
    except Exception as e:
        exec debug_s


# http://stackoverflow.com/questions/19514288/locals-and-globals-in-stack-trace-on-exception-python
# 当异常发生的时候输出locals的结果用来调试
from pprint import pprint
import sys, traceback
from pprint import pprint, pformat

def excepthook(type, value, tb):
    traceback.print_exception(type, value, tb)

    while tb.tb_next:
        tb = tb.tb_next

    print >>sys.stderr, 'Locals:\n',  pformat(tb.tb_frame.f_locals)
    #print >>sys.stderr, 'Globals:', tb.tb_frame.f_globals

sys.excepthook = excepthook

def x():
    x = 1
    y()

def y():
    foo = 1
    bar = 0
    d = {a:0 for a in range(30)}

    foo/bar

x()



# https://benjamin-schweizer.de/improved-python-traceback-module.html
import tracebackturbo as traceback

def erroneous_function():
    ham = u"unicode string with umlauts äöü."
    eggs = "binary string with umlauts äöü."
    i = 23
    if i>5:
        raise Exception("it's true!")

try:
    erroneous_function()
except:
    print traceback.format_exc(with_vars=True)
