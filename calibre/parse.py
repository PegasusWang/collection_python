# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def main():
    domain = "http://learn.lianglianglee.com"
    site = "http://learn.lianglianglee.com/%E4%B8%93%E6%A0%8F/Redis%20%E6%A0%B8%E5%BF%83%E5%8E%9F%E7%90%86%E4%B8%8E%E5%AE%9E%E6%88%98/01%20Redis%20%E6%98%AF%E5%A6%82%E4%BD%95%E6%89%A7%E8%A1%8C%E7%9A%84.md"

    resp = requests.get(url)
    resp.encoding='utf-8'
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    uls = soup.find_all("ul")
    links = uls[2].find_all('a')
    for link in links:
        title = link.get_text()
        print(link.get('href'), title)

if __name__ == "__main__":
    main()
