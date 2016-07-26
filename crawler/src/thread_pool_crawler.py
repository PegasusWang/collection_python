#!/usr/bin/env python
# -*- coding:utf-8 -*-


import concurrent.futures
import bs4
import requests


class ThreadPoolCrawler(object):
    def __init__(self, urls, concurrency=20, **kwargs):
        self.urls = urls
        self.concurrency = min(concurrency, len(urls))
        self.results = []

    def handle_response(self, url, response):
        print(url)
        print(response.status_code)

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
                    # import traceback
                    # traceback.print_exc()
                    print(e)
                else:
                    self.handle_response(url, response)


class TestCrawler(ThreadPoolCrawler):
    def handle_response(self, url, response):
        print(url, response.status_code)
        pass
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        title = soup.find('title')
        self.results.append({url: title})


def main():
    import time
    urls = ['http://localhost:8000/test'] * 100
    for nums in [5, 10, 15, 20, 50, 70, 100]:
        beg = time.time()
        s = TestCrawler(urls, nums)
        s.run()
        print(nums, time.time()-beg)


def test():
    #urls = ['http://localhost:8000/test'] * 5
    urls = ['http://www.baidu.com'] * 5
    s = TestCrawler(urls)
    s.run()


if __name__ == '__main__':
    # main()
    test()
