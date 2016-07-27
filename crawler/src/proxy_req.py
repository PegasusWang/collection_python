#!/usr/bin/env python
# -*- coding:utf-8 -*-


# requests proxy demo
import requests


def use_lantern():
	# install lantern first, 这是使用lantern的代理地址
	proxies = {
		"http": "http://127.0.0.1:8787",
		"https": "http://127.0.0.1:8787",
	}

	url = 'http://httpbin.org/ip'
	r = requests.get(url, proxies=proxies)
	print(r.text)


def user_socks5():
	# requests from version 2.10.0 support socks proxy
	# pip install -U requests[socks]
	proxies = {'http': "socks5://myproxy:9191"}
	requests.get('http://example.org', proxies=proxies)

	# tornado proxy demo
	# sudo apt-get install libcurl-dev librtmp-dev
	# pip install tornado pycurl


def tornado_proxy():
	from tornado import httpclient, ioloop

	config = {
		'proxy_host': 'YOUR_PROXY_HOSTNAME_OR_IP_ADDRESS',
		'proxy_port': 3128
	}

	httpclient.AsyncHTTPClient.configure(
		"tornado.curl_httpclient.CurlAsyncHTTPClient")


	def handle_request(response):
		if response.error:
			print "Error:", response.error
		else:
			print response.body
		ioloop.IOLoop.instance().stop()

	http_client = httpclient.AsyncHTTPClient()
	http_client.fetch("http://twitter.com/",
		handle_request, **config)
	ioloop.IOLoop.instance().start()


def get_proxy_dict(ip, port, proxy_type='http' or 'socks5'):
    """get_proxy_dict return dict proxies as requests proxies
    http://docs.python-requests.org/en/master/user/advanced/

    :param ip: ip string
    :param port: int port
    :param proxy_type: 'http' or 'socks5'
    """
    proxies = {
        'http': '{proxy_type}://{ip}:{port}'.format(proxy_type=proxy_type, ip=ip, port=port),
        'https': '{proxy_type}://{ip}:{port}'.format(proxy_type=proxy_type, ip=ip, port=port),
    }
    return proxies


def requests_proxy(ip, port):
    proxies = get_proxy_dict(ip, port)
    url = 'http://httpbin.org/ip'
    r = requests.get(url, proxies=proxies, timeout=10)
    print(r.text)


if __name__ == '__main__':
    requests_proxy('101.201.235.141', 8000)
    requests_proxy('171.39.28.231', 8123)
