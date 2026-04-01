#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
递归统计一个目录下所有视频文件的总时长。比如笔者用来统计课程的内容总时长。

pip install moviepy

如果安装报错，尝试升级

pip install --upgrade setuptools

使用方法：
python compute_duration.py --path ~/Movies/ --type .mp4

参考：https://blog.csdn.net/qq_22210253/article/details/86684658
"""

import os
import datetime
import argparse
from moviepy.editor import VideoFileClip


def main():
    parser = argparse.ArgumentParser(
        description='Compute Total Time of a Series of Videos')
    parser.add_argument("--path", metavar="PATH", default=".",
                        help="the root path of the videos(default: .)")
    parser.add_argument("--type", metavar="TYPE", default=".mkv",
                        help="the type of the videos(default: .mkv)")
    args = parser.parse_args()
    filelist = []
    for root, dirs, files in os.walk(args.path):
        for name in files:
            fname = os.path.join(root, name)
            if fname.endswith(args.type):
                filelist.append(fname)
    ftime = 0.0
    for file in sorted(filelist):
        clip = VideoFileClip(file)
        print("{}: {}秒".format(file, clip.duration))
        ftime += clip.duration
    print("%d seconds: " % ftime, str(datetime.timedelta(seconds=ftime)))


if __name__ == "__main__":
    main()
