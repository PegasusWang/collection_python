#!/usr/bin/env python
# -*- coding:utf-8 -*-
import concurrent.futures
import bs4
import requests


class ThreadPoolCrawler(object):
    def __init__(self, urls, concurrency=10, **kwargs):
        self.urls = urls
        self.concurrency = concurrency
        self.results = []

    def handle_response(self, url, response):
        pass

    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs)

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            future_to_url = {
                executor.submit(self.get, url): url for url in self.urls
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    response = future.result()
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                else:
                    self.handle_response(url, response)


class TestCrawler(ThreadPoolCrawler):
    def handle_response(self, url, response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        title = soup.find('title')
        self.results.append({url: title})


def main():
    import time
    urls = ['http://localhost:8000'] * 300
    for nums in [2, 5, 10, 15, 20, 50, 70, 100]:
        beg = time.time()
        s = TestCrawler(urls, nums)
        s.run()
        print(nums, time.time()-beg)

if __name__ == '__main__':
    main()
