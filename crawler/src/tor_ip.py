#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import requests
import requesocks

#url = 'https://api.ipify.org?format=json'
url = 'http://httpbin.org/ip'


def get_ip_socks_tor():
    cmd = """curl --socks5 127.0.01:9050 http://checkip.amazonaws.com/"""
    os.system(cmd)


def getip_requests(url):
    print "(+) Sending request with plain requests..."
    r = requests.get(url)
    print "(+) IP is: " + r.text.replace("\n", "")


def getip_requesocks(url):
    print "(+) Sending request with requesocks..."
    session = requesocks.session()
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    r = session.get(url)
    print "(+) IP is: " + r.text.replace("\n", "")


def tor_requests():
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050',
    }
    r = requests.get(url, proxies=proxies)
    print r.text


def main():
    print "Running tests..."
    getip_requests(url)
    getip_requesocks(url)
    os.system("""(echo authenticate '"yourpassword"'; echo signal newnym; echo quit) | nc localhost 9051""")
    getip_requesocks(url)


if __name__ == "__main__":
    main()
    #tor_requests()
