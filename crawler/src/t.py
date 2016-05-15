import urllib2
from proxy_urllib2 import SocksHandler

proxy_addr_ip = ('45.79.153.90', 18436L)

url = 'https://api.ipify.org?format=json'

opener = urllib2.build_opener(SocksHandler(*proxy_addr_ip))
print(opener.open(url).read())


proxy_addr_ip = ('45.33.92.71', 18436L)
opener = urllib2.build_opener(SocksHandler(*proxy_addr_ip))
print(opener.open(url).read())
