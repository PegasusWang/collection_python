#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 1. 安装必备库moviepy
# pip install moviepy -i https://pypi.tuna.tsinghua.edu.cn/simple

# 2. 写入代码

from moviepy.editor import *

clip = (VideoFileClip("movie.mp4"))  # 需要转为GIF的视频文件路径
clip.write_gif("movie.gif")

# 4. GIF很大的解决方案
# 我们除了设置缩放分辨率resize外，还可以通过设置fps参数抽帧来减少大小

from moviepy.editor import *

clip = (VideoFileClip("movie.mp4").resize((488,225)))
clip.write_gif("movie.gif",fps=15)  #设置为每秒15帧

# 设置为每秒15帧后，文件大小只有2m多，一下缩小了4倍之多！

# 5. 截取视频长度转换
# 我们还可以通过设置subclip参数来指定转换的视频范围:
#
# subclip：截取原视频中的自t_start至t_end间的视频片段
#
# 将视频1-2秒片段转化为Gif


from moviepy.editor import *

clip = (VideoFileClip("movie.mp4").subclip(t_start=1, t_end=2).resize((488, 225)))
clip.write_gif("movie.gif", fps=15)

# 6. 指定转换后的图片大小（分辨率）
# resize参数可指定转换后的图片大小
#
# 接受的参数为：
#
# 以像素或浮点表示的(width,height)
#
# 缩放百分比，如 0.5
#
# 示例
#
# 1.设置转换后的图片为600*400
#
clip = (VideoFileClip("movie.mp4").resize((600, 400)))
clip.write_gif("movie.gif", fps=15)

# 2.原视频缩放50%
#
clip = (VideoFileClip("movie.mp4").resize(0.5))
clip.write_gif("movie.gif", fps=15)

