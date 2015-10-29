#!/usr/bin/env python
# -*- coding:utf-8 -*-


from earth import PID2NAME
from school import SCHOOL_UNIVERSITY
from io import open


def solve_china_city():
    with open('china_city.txt', 'r', encoding="utf-8") as f:
        for l in f:
            l = l.strip()
            unicode.endswith
            if l.endswith(tuple(['市', '区', '县'])):
                print l[:-1]
            else:
                print l


def solve_school():
    for k, v in SCHOOL_UNIVERSITY.iteritems():
        print v
    print(len(SCHOOL_UNIVERSITY))


#solve_school()
solve_china_city()
