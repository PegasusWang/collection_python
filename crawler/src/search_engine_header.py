#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 模仿百度蜘蛛
import requests

url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
}
r = requests.get(url, headers=headers)
print(r.text)
'''
Baiduspider:
Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)


google:
Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
'''

UA_LIST = [
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; bingbot/2.0 +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
]
