#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""ping脚本，有新文章发布的时候通知搜索引擎"""


import json
import xmlrpclib
from db import redis
from single_process import single_process


def ping(ping_url, site_name, site_host, post_url, rss_url):
    rpc_server = xmlrpclib.ServerProxy(ping_url)
    result = rpc_server.weblogUpdates.extendedPing(
        site_name, site_host, "http://"+post_url, "http://"+rss_url
    )
    print result


def ping_all(*args, **kwds):
    ping_url_list = [
        'http://ping.baidu.com/ping/RPC2',
        'http://rpc.pingomatic.com/',
        'http://blogsearch.google.com/ping/RPC2',
    ]
    print args
    for url in ping_url_list:
        ping(url, *args, **kwds)


@single_process
def main():
    client = redis.pubsub()
    client.subscribe(['ping'])
    while True:
        print "."
        for item in client.listen():
            print item
            if item['type'] == 'message':
                msg = item['data']
                if msg:
                    ping_all( * tuple( json.loads(msg) ) )


def test():
    site_name = "tech2ipo"
    site_host = "http://alpha.tech2ipo.com"
    post_url = 'http://alpha.tech2ipo.com/100855'
    rss_url = "http://alpha.tech2ipo.com/rss/alpha.tech2ipo.com"
    ping_all(site_name, site_host, post_url, rss_url)


if __name__ == '__main__':
    #test()
    main()
