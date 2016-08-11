#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 并行执行命令
from subprocess import Popen

commands = [
    'date; ls -l; sleep 1; date',
    'date; sleep 5; date',
    'date; df -h; sleep 3; date',
    'date; hostname; sleep 2; date',
    'date; uname -a; date',
]
# run in parallel
processes = [Popen(cmd, shell=True) for cmd in commands]
# do other things here..
# wait for completion
for p in processes: p.wait()
