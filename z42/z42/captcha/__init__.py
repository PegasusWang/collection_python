#!/usr/bin/env python
#coding:utf-8
from random import choice
import captchaimage
from PIL import Image
import sys
from cStringIO import StringIO
from base64 import b64encode
from os.path import dirname, join

CHARSET = 'ABCEDEFJHIJKMNPQRSTUVWXYZ23456789'
FONT_PATH = join(dirname(__file__),"r.ttf")

def captcha(size_y=40):
    text=''.join(choice(CHARSET) for i in xrange(5))
    image_data = captchaimage.create_image(
           FONT_PATH,30,size_y,
           text
           )

    image = Image.fromstring(
           "L", (len(image_data) / size_y, size_y), image_data)

    f = StringIO()
    image.save(f,"PNG")
    return text, b64encode(f.getvalue())

if __name__ == "__main__":
    for i in range(100):
        print captcha() 



