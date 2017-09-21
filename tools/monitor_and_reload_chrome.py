#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
监控文件变动刷新浏览器，前端框架支持浏览器自动刷新，这里用 python 实现，方便写前端页面的时候看到修改效果
http://sakthipriyan.com/2016/02/15/auto-refresh-chrome-when-files-modified.html
"""

import asyncore
import json
import os
import subprocess
import threading

import pyinotify
import requests
from imagine import imagine
from websocket import create_connection


# Look for only these two events.
mask = pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE

# Custom class to process the Event.


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, fn, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.function = fn

    def process_IN_DELETE(self, event):
        self.function()

    def process_IN_CLOSE_WRITE(self, event):
        self.function()

# this method will monitor the given directory
# it calls the callback() when the monitored event occurs.


def monitor(directory, callback):
    wm = pyinotify.WatchManager()
    # rec=True, to monitor all sub directories recursively.
    # auto_add=True, to monitor added new sub directories.
    wm.add_watch(directory, mask, rec=True, auto_add=True)
    # specify the event handler to process the events.
    pyinotify.AsyncNotifier(wm, EventHandler(callback))
    # start the asyncore loop to monitor and process events.
    asyncore.loop()


chrome_port = 9222
chrome_json_url = 'http://localhost:%s/json' % (chrome_port)
refresh_json = json.dumps({
    "id": 0,
    "method": "Page.reload",
    "params": {"ignoreCache": True}
})


def open_browser(url):
    # directory is used by Google Chrome to store profile for this remote user.
    directory = os.path.expanduser('~/.chrome-remote-profile')
    command = 'google-chrome --remote-debugging-port=%d --user-data-dir=%s %s' % \
        (chrome_port, directory, url)
    subprocess.call(command, shell=True)


def refresh_browser():
    # get response for the GET request.
    response = requests.get(chrome_json_url)
    # Process each item in the response.
    for page in response.json():
        # only if it is a page and interested urls.
        if page['type'] == 'page' and 'localhost:8000' in page['url']:
            # Open websocket connection, send json and close it.
            # This will refresh this specific tab.
            ws = create_connection(page['webSocketDebuggerUrl'])
            ws.send(refresh_json)
            ws.close()


def start_browser():
    # Browser is launched via a daemon thread.
    # It will terminate the browser when you close the python script.
    thread = threading.Thread(target=open_browser, kwargs={'url': 'http://localhost:8000'})
    thread.daemon = True
    thread.start()


# Import imagine function from a imagine file.

# Callback does two things, as promised.


def cb():
    imagine()  # Step 4.1
    refresh_browser()  # Step 4.2


if __name__ == "__main__":
    my_directory = './templates'
    # Set up for first time.
    imagine()  # Step 1
    start_browser()  # Step 2
    monitor(my_directory, cb)  # Step 3
