#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
import os


def watermark(mark, path, savepath):
    '''
    给图片加文字水印
    mark 水印文字 String
    path 图片名称 String
    savepath 保存路径 String
    '''
    # 打开等待加水印的图片
    image = Image.open(path)
    # 打开水印图片
    watermark = Image.open(mark)
    # 如果觉得水印图片太大，可以缩放，这里缩放比例为50%
    factor = 0.5
    # 缩放图片
    watermark = watermark.resize(tuple(map(lambda x: int(x * factor), watermark.size)))
    # 生成一个新的layer
    layer = Image.new('RGBA', image.size)
    # 把水印打到新的layer上去，后面参数是水印位置，此处是右下角
    layer.paste(watermark, (image.size[0] - watermark.size[0], image.size[1] - watermark.size[1]))
    # 更多位置参考上面的代码
    # 添加水印
    marked_img = Image.composite(layer, image, layer)
    # 保存图片
    marked_img.save(os.path.join(savepath, os.path.basename(path)))
    # 打开生成的图片（缓存图片）
    marked_img.show()


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
    mark = 'qrcode.jpg'
    for path in paths:
        watermark(mark, path, "D:\\watermark")
    print('Done!')
