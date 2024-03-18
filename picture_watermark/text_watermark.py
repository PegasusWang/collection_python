#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

# 打开要加水印的图片
image = Image.open('lifeistoshort.jpg')
# 提示要打水印的文字
text = input('输入你的水印文字:\n')
# 获得一个字体，你也可以自己下载相应字体，第二个值是字体大小
font = ImageFont.truetype('C:\Windows\Fonts\simhei.ttf', 64)
# 将图片转换为RGBA图片
layer = image.convert('RGBA')
# 依照目标图片大小生成一张新的图片 参数[模式,尺寸,颜色(默认为0)]
text_overlay = Image.new('RGBA', layer.size)
# 画图
image_draw = ImageDraw.Draw(text_overlay)
# 获得字体大小,textsize(text, font=None)
text_size_x, text_size_y = image_draw.textsize(text, font=font)
# 设置文本位置 此处是右下角显示
# text_xy = (layer.size[0] - text_size_x, layer.size[1] - text_size_y)

# 设置文本位置 此处是下方居中显示
# text_xy = (layer.size[0]//2-text_size_x//2, layer.size[1]-text_size_y)

# 设置文本位置 此处是左下角下角显示
# text_xy = (0, layer.size[1]-text_size_y)

# 设置文本位置 此处是右上角显示
# text_xy=(layer.size[0]-text_size_x,0)

# 设置文本位置 此处是左上角角显示
# text_xy=(0,0)

# 设置文本位置 此处是居中显示
text_xy = (layer.size[0]//2-text_size_x//2, layer.size[1]//2-text_size_y//2)


# 设置文字，位置,字体,颜色和透明度
image_draw.text(text_xy, text, font=font, fill=(0, 0, 0, 85))
# 将水印打到原图片上生成新的图片
marked_img = Image.alpha_composite(layer, text_overlay)
# 保存图片
marked_img.save('new_after.png')
# 显示图片（这里是生成一个临时文件，必须关闭图片 这段py代码才算结束）
marked_img.show()

