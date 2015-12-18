#!/usr/bin/env python
#coding:utf-8
import _env
import gearman as _gearman
from z42.gearman import GearmanServer

GM_WORKER = _gearman.GearmanWorker(['localhost:4730'])
gearman = GearmanServer(GM_WORKER)

