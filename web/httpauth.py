# -*- coding: utf-8 -*-


"""
python http auth 示例

https://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
"""

import requests
from http.client import HTTPSConnection
from base64 import b64encode


def test1():
    r = requests.get('https://my.website.com/rest/path', auth=('myusername', 'mybasicpass'))
    print(r.text)


def test2():
    #This sets up the https connection
    c = HTTPSConnection("www.google.com")
    #we need to base 64 encode it
    #and then decode it to acsii as python 3 stores it as a byte string
    userAndPass = b64encode(b"username:password").decode("ascii")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass }
    #then connect
    c.request('GET', '/', headers=headers)
    #get the response back
    res = c.getresponse()
    # at this point you could check the status etc
    # this gets the page text
    data = res.read()
