#!/usr/bin/env python
#coding:utf-8
import _env
import gearman as _gearman
from z42.gearman import GearmanClient

GM_CLIENT = _gearman.GearmanClient(['localhost:4730'])
gearman = GearmanClient(GM_CLIENT)

