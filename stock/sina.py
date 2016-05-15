#! /usr/bin/python3
# coding=utf-8

'''
Created on Nov 9, 2011

@author: 笑遍世界
'''

import urllib.request

def get_price(code):
       url = 'http://hq.sinajs.cn/?list=%s' % code
       req = urllib.request.Request(url)
#如果不需要设置代理，下面的set_proxy就不用调用了。由于公司网络要代理才能连接外网，所以这里有set_proxy…
       content = urllib.request.urlopen(req).read()
       str = content.decode('gbk')
       data = str.split('"')[1].split(',')
       name = "%-6s" % data[0]
       price_current = "%-6s" % float(data[3])
       change_percent = ( float(data[3])-float(data[2]) )*100 / float(data[2])
       change_percent = "%-6s" % round (change_percent, 2)
       print("股票名称:{0} 涨跌幅:{1} 最新价:{2}".format(name, change_percent, price_current) )

def get_all_price(code_list):
   for code in code_list:
       get_price(code)

code_list = ['sz300036', 'sz000977', 'sh600718', 'sh600452', 'sh600489']
get_all_price(code_list)
