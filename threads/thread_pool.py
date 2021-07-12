#!/usr/bin/env python
# -*- coding:utf-8 -*-

try:
    import Queue
except ImportError:
    import queue as Queue
import sys
import requests
import os
import threading
import time
from bs4 import BeautifulSoup


class Worker(threading.Thread):    # 处理工作请求
    def __init__(self, workQueue, resultQueue, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue

    def run(self):
        while 1:
            try:
                callable, args, kwds = self.workQueue.get(False)    # get task
                res = callable(*args, **kwds)
                self.resultQueue.put(res)    # put result
            except Queue.Empty:
                break


class WorkManager:    # 线程池管理,创建
    def __init__(self, num_of_workers=10):
        self.workQueue = Queue.Queue()    # 请求队列
        self.resultQueue = Queue.Queue()    # 输出结果的队列
        self.workers = []
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue)    # 创建工作线程
            self.workers.append(worker)    # 加入到线程队列

    def start(self):
        for w in self.workers:
            w.start()

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()    # 从池中取出一个线程处理请求
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)    # 重新加入线程池中
        print('All jobs were complete.')

    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))    # 向工作队列中加入请求

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)


def download_file(url):
    """这里可以请求并保存网页"""
    #print 'beg download', url
    print(BeautifulSoup(requests.get(url).content).find('title'))


def main():
    try:
        num_of_threads = int(sys.argv[1])
    except:
        num_of_threads = 10
    _st = time.time()
    wm = WorkManager(num_of_threads)
    print(num_of_threads)
    urls = []
    n = 1000
    for page in range(1, n):
        urls.append('http://www.jb51.net/article/%s.htm' % page)
    for i in urls:
        wm.add_job(download_file, i)
    wm.start()
    wm.wait_for_complete()
    print(time.time() - _st)

if __name__ == '__main__':
    main()
