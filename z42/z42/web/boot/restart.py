#!/usr/bin/env python
#coding:utf-8
import _env
import envoy
import sys
from os.path import abspath, dirname, join
from z42.config import HOST 
from z42.config import APP


std_out = envoy.run("supervisorctl status").std_out
print APP
print std_out
for i in std_out.split("\n"):

    i = i.split(" ",1)[0].strip()
    if i:
        if HOST in i:
            cmd = "sudo supervisorctl restart %s"%i
            print cmd
            envoy.run(cmd)

