#!/usr/bin/env python
# coding:utf-8


def iunique(iterable, key=None):
    seen = set()
    for i in iterable:
        t = i
        if key is not None:
            t = key(i)
        if t not in seen:
            seen.add(t)
            yield i


def unique(iterable):
    return list(iunique(iterable))


def inplace_unique_extend(*args):
    first = args[0]
    seen = set(first)
    for iterable in args[1:]:
        for i in iterable:
            if i not in seen:
                seen.add(i)
                first.append(i)
    return first
