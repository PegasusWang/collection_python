#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
监控文件改动后自动重启进程的脚本，依赖pyinotify, colorama
"""
# http://buke.github.io/blog/2013/06/30/reload-the-process-when-source-chage-is-detected/
# pip install pyinotify, colorama

import os
from pprint import pprint
import signal
import subprocess
import time

import pyinotify
from colorama import Fore, Style    # for color terminal print
from pyinotify import log
TERMINAL_COLOR = 'RED'


class ReloadNotifier(pyinotify.Notifier):
    def loop(self, callback=None, daemonize=False, **args):
        if daemonize:
            self.__daemonize(**args)

        # Read and process events forever
        while 1:
            try:
                self._default_proc_fun._print_stdout()
                self.process_events()
                if (callback is not None) and (callback(self) is True):
                    break
                ref_time = time.time()
                # check_events is blocking
                if self.check_events():
                    self._sleep(ref_time)
                    self.read_events()
            except KeyboardInterrupt:
                # Stop monitoring if sigint is caught (Control-C).
                log.debug('Pyinotify stops monitoring.')
                self._default_proc_fun._stop_process()
                break
        # Close internals
        self.stop()


class OnChangeHandler(pyinotify.ProcessEvent):

    def my_init(self, cwd, extension, cmd):
        self.cwd = cwd
        self.extensions = [ext for ext in extension.split(',') if ext]
        self.cmd = cmd
        self.process = None
        self._start_process()

    def _start_process(self):
        self.process = subprocess.Popen(self.cmd, shell=True,
                                        preexec_fn=os.setsid)

    def _stop_process(self):
        # os.killpg(self.process.pid, signal.SIGTERM)
        os.killpg(self.process.pid, signal.SIGKILL)
        self.process.wait()

    def _restart_process(self):
        self._stop_process()
        self._start_process()

    def _print_stdout(self):
        stdout = self.process.stdout
        if stdout is not None:
            print(stdout)

    def process_IN_CREATE(self, event):
        if (any(event.pathname.endswith(ext) for ext in self.extensions) or
            "IN_ISDIR" in event.maskname):
            print(getattr(Fore, TERMINAL_COLOR) +
                  event.pathname + ' ' + event.maskname + '\n' +
                  'restart process' +
                  time.strftime('%Y-%m-%d %A %X %Z',
                                time.localtime(time.time())))
            print(Style.RESET_ALL)
            self._restart_process()

    process_IN_DELETE = process_IN_CLOSE_WRITE = process_IN_CREATE
    process_IN_MOVED_FROM = process_IN_CLOSE_WRITE
    process_IN_MOVED_TO = process_IN_CLOSE_WRITE


def autoreload(path, extension, cmd, excl_list):
    wm = pyinotify.WatchManager()
    handler = OnChangeHandler(cwd=path, extension=extension, cmd=cmd)
    notifier = ReloadNotifier(wm, default_proc_fun=handler)
    # https://github.com/seb-m/pyinotify/blob/master/python2/examples/exclude.py
    excl = pyinotify.ExcludeFilter(excl_list)    # exclude file

    # 设置需要监控的事件
    mask = (pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_FROM |
            pyinotify.IN_MOVED_TO | pyinotify.IN_CREATE | pyinotify.IN_DELETE |
            pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVE_SELF |
            pyinotify.IN_MODIFY)
    wm.add_watch(path, mask, rec=True, auto_add=True,
                 exclude_filter=excl)

    print(getattr(Fore, TERMINAL_COLOR) +
          '==> Start monitoring %s (type c^c to exit) <==' % path +
          time.strftime('%Y-%m-%d %A %X %Z', time.localtime(time.time())))
    print(Style.RESET_ALL)
    notifier.loop()


if __name__ == '__main__':
    import sys
    path = './webapp/'
    excl_list = ['./webapp/node_modules/*', './webapp/assets/*']
    extension = 'py,'
    try:
        port = sys.argv[1]
    except IndexError:
        port = '1200'
    cmd = """python manage.py server"""
    autoreload(path, extension, cmd, excl_list)
