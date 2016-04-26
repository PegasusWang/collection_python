#!/usr/bin/env python
# -*- coding:utf-8 -*-


def select_middle(num_list):
    length = len(num_list)
    if length <= 3:
        return num_list[0]

    mid = int(length/2)
    a = num_list[0]
    b = num_list[-1]
    c = num_list[mid]
    return a + b + c - max(a, b, c) - min(a, b, c)


def swap(a, b):
    a, b = b, a


def qsort(seq):
    less = []
    equal = []
    greater = []

    if len(seq) > 1:
        pivot = select_middle(seq)
        for num in seq:
            if num < pivot:
                less.append(num)
            elif num == pivot:
                equal.append(num)
            else:
                greater.append(num)
        return qsort(less) + equal + qsort(greater)
    else:
        return seq


def test_qsort():
    from random import shuffle
    l = list(range(10))
    shuffle(l)
    print(qsort(l))
    assert qsort(l) == list(range(10))
    assert 0

test_qsort()
