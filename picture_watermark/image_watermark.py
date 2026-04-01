#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image

# 打开等待加水印的图片
image = Image.open('lifeistoshort.jpg')
# 打开水印图片
watermark = Image.open('qrcode.jpg')
# 如果觉得水印图片太大，可以缩放，这里缩放比例为50%
factor = 0.5
# 缩放图片
watermark = watermark.resize(tuple(map(lambda x: int(x * factor), watermark.size)))
# 生成一个新的layer
layer = Image.new('RGBA', image.size)
# 把水印打到新的layer上去，后面参数是水印位置，此处是右下角
layer.paste(watermark, (image.size[0] - watermark.size[0], image.size[1] - watermark.size[1]))
# 添加水印
marked_img = Image.composite(layer, image, layer)
# 保存图片
marked_img.save('maked_lifeistoshort_1.jpg')
# 打开生成的图片（缓存图片）
marked_img.show()