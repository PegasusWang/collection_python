#!/usr/bin/env python
#coding:utf-8
import _env
from z42.web.mysql.orm.kv import Kv


ObCid = Kv('ObCid')

if __name__ == "__main__":
    print ObCid.get(100000083)
    ObCid.set(1,2)

