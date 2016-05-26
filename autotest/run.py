#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://buke.github.io/blog/2013/06/30/reload-the-process-when-source-chage-is-detected/
# pip install pyinotify

import os
import signal
import subprocess
import time
import pyinotify
from pyinotify import log


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

    def __init__(self, cwd, extension, cmd):
        self.cwd = cwd
        self.extensions = extension.split(',')
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
        print('==> Modification detected, restart process. <==')
        self._stop_process()
        self._start_process()

    def _print_stdout(self):
        stdout = self.process.stdout
        if stdout is not None:
            print(stdout)

    def process_IN_CREATE(self, event):
        if (any(event.pathname.endswith(ext) for ext in self.extensions) or
            "IN_ISDIR" in event.maskname):
            self._restart_process()

    process_IN_DELETE = process_IN_CLOSE_WRITE = process_IN_CREATE
    process_IN_MOVED_FROM = process_IN_CLOSE_WRITE
    process_IN_MOVED_TO = process_IN_CLOSE_WRITE


def autoreload(path, extension, cmd):
    wm = pyinotify.WatchManager()
    handler = OnChangeHandler(cwd=path, extension=extension, cmd=cmd)
    notifier = ReloadNotifier(wm, default_proc_fun=handler)

    mask = (pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_FROM |
            pyinotify.IN_MOVED_TO | pyinotify.IN_CREATE | pyinotify.IN_DELETE |
            pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVE_SELF)
    wm.add_watch(path, mask, rec=True, auto_add=True)

    print('==> Start monitoring %s (type c^c to exit) <==' % path)
    notifier.loop()


if __name__ == '__main__':
    path = './'
    extension = 'py,mako'
    cmd = """uwsgi --http :1200 --wsgi-file wsgi_test.py --honour-stdin -m -p 2 --http-keepalive --http-timeout 180"""
    autoreload(path, extension, cmd)
