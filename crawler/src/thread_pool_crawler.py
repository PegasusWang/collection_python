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
        print(soup.find('title'))


def main():
    urls = ['http://www.baidu.com'] * 100
    s = TestCrawler(urls)
    s.run()

if __name__ == '__main__':
    main()
