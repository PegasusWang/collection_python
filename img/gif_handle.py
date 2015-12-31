#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""把gif连接成一个长图, 类似百度机器人的动画"""

from PIL import Image


class ImageSequence(object):
    def __init__(self, im):
        self.im = im

    def __getitem__(self, ix):
        try:
            if ix:
                self.im.seek(ix)
            return self.im
        except EOFError:
            self.im.seek(0)
            raise IndexError  # end of sequence


class GifHandler(object):
    def __init__(self, filepath):
        self.im = Image.open(filepath)
        self.image_seq = ImageSequence(self.im)

    def handle_frame(self, index, frame):
        print(frame.size)
        print(frame.mode)
        print(frame.format)

    def handle_all(self):
        width = self.im.size[0]
        height = self.im.size[1]
        length = len(list(self.image_seq))
        blank_img = Image.new('RGB', (width*length, height))

        for index, im in enumerate(self.image_seq):
            blank_img.paste(im, (width*index, 0))

        blank_img.show()
        blank_img.thumbnail((148*length, 148), Image.ANTIALIAS)
        blank_img.save('./ren.png')


def main():
    filepath = './t.gif'
    h = GifHandler(filepath)
    h.handle_all()


if __name__ == '__main__':
    main()
