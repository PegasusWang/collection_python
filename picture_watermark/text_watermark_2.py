#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os


def watermark(text, filename, savepath):
    '''
    给图片加文字水印
    text 水印文字 String
    filename 图片名称 String
    savepath 保存路径 String
    '''
    # 检查保存文件夹是否存在，如果不存在则生成一个
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    # 打开要加水印的图片
    image = Image.open(filename)
    # 获得一个字体，你也可以自己下载相应字体，第二个值是字体大小
    font = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 64)
    # 将图片转换为RGBA
    layer = image.convert('RGBA')
    # 依照目标图片大小生成一张新的图片 参数[模式,尺寸,颜色(默认为0)]
    text_overlay = Image.new('RGBA', layer.size)
    # 画图
    image_draw = ImageDraw.Draw(text_overlay)
    # 获得字体大小,textsize(text, font=None)
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本位置 此处是右下角显示
    text_xy = (layer.size[0] - text_size_x, layer.size[1] - text_size_y)
    # 设置文字，位置,字体,颜色和透明度
    image_draw.text(text_xy, text, font=font, fill=(0, 0, 0, 85))
    # 将水印打到原图片上生成新的图片
    marked_img = Image.alpha_composite(layer, text_overlay)
    # 保存图片
    marked_img.save(os.path.join(savepath, os.path.basename(filename).split('.')[0] + ".png"))


def all_path(dirname, filters):
    '''
    获取路径下所有文件名称（完整路径）
    dirname 路径名 String
    filters 过滤文件类型 Array
    '''
    result = []  # 所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        # maindir 当前主目录
        # subdir 当前主目录下的所有目录
        # file_name_list 当前主目录下的所有文件
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            ext = os.path.splitext(apath)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容
            if ext in filters:
                result.append(apath)
    return result


if __name__ == '__main__':

    filters = [".jpg", ".jpeg", ".png"]  # 设置过滤后的文件类型
    paths = all_path(r"C:\Users\liming\Downloads\mytest", filters)
    text = input('输入你的水印文字:\n')
    for path in paths:
        watermark(text, path, r"D:\watermark")
    print('Done!')
