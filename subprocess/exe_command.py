#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from threading import Timer


def exe_command(cmd, timeout=300):
    # https://stackoverflow.com/questions/1191374/using-module-subprocess-with-timeout
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timer = Timer(timeout, process.kill)
    try:
        timer.start()
        stdout, stderr = process.communicate()
        shellresult = stdout.decode('utf-8', errors='ignore')
        retcode = process.poll()
        return (retcode, shellresult)
    finally:
        timer.cancel()


if __name__ == '__main__':
    print(exe_command('ifconfig'))
