#!/usr/bin/env python
#coding:utf-8
import _env
from _gearman import gearman
from zapp.SITE.model.index import index as _index
index = gearman.async(_index)


