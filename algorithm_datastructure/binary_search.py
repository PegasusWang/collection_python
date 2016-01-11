#!/usr/bin/env python
# -*- coding:utf-8 -*-


def bsearch(l, to_search):
    beg = 0
    end = len(l) - 1
    while beg < end:
        mid = beg + int((end - beg) / 2)
        if l[mid] < to_search:
            beg = mid + 1
        elif l[mid] > to_search:
            end = mid
        else:
            return mid
    return -1


def test():
    l = list(range(10))
    assert bsearch(l, 1) == 1
    assert bsearch(l, 0) == 0
    assert bsearch(l, 10) == -1
