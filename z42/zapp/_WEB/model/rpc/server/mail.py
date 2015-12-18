#!/usr/bin/env python
#coding:utf-8
import _env
from _gearman import gearman
from z42.web.mail import rendermail as _rendermail

rendermail = gearman.async(_rendermail)


