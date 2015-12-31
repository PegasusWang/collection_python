#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

import aiohttp
import asyncio
import time


class Retriever:
    def __init__(self, urls):
        self.results = list()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run(urls))

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.results) == 0:
            raise StopIteration
        return self.results.pop(0)


    def fetch_page(self, url, idx):
        try:
            response = yield from aiohttp.request('GET', url)
        except aiohttp.errors.ClientResponseError:
            print("[-]aiohttp.errors.ClientResponseError, pausing and continuing...")
            time.sleep(1)
            response = yield from aiohttp.request('GET', url)
        if response.status == 200:
            print("[+] Data fetched successfully for page: " + str(idx+1))
            self.results.append(response)
        else:
            print("[-] Data fetch failed for: %d" % idx)
            print(response.content, response.status)
        response.close()

    def run(self, urls):
        coros = []
        for idx, url in enumerate(urls):
            coros.append(asyncio.Task(self.fetch_page(url, idx)))

        yield from asyncio.gather(*coros)


def main():
    urls = []
    for i in range(100):
        urls.append('http://www.jb51.net/%d.htm' % i)
    Retriever(urls)

if __name__ == '__main__':
    main()
