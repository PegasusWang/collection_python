#!/usr/bin/env python
# -*- coding:utf-8 -*-


def qsort(seq):
    if not seq:
        return seq
    else:
        pivot = seq[0]
        lesser = qsort([x for x in seq[1:] if x < pivot])
        greater = qsort([x for x in seq[1:] if x >= pivot])
        return lesser + [pivot] + greater


def test_qsort():
    from random import shuffle
    l = list(range(10))
    shuffle(l)
    assert qsort(l) == list(range(10))
