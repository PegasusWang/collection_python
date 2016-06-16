#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, signal

def kill_process_name(process_name):
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
        if name in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)


if __name__ == '__main__':
    pass
