#!/usr/bin/env python
# -*- coding:utf-8 -*-


def dos2unix(filename):
    text = open(filename, 'rb').read().replace('\r\n', '\n')
    open(filename, 'wb').write(text)


def to_utf8(filename):
    txt = open(filename, 'r').read()
    with open(filename, 'w') as f:
        if 'charset=gb2312' in txt.lower():
            txt = txt.decode('gb2312')
        else:
            txt = txt.decode('gbk')
        f.write(txt.encode('utf-8'))

#暂时不用转成utf－8，抠出来想要得信息,其他不用管
def main():
    filename = './t.html'
    fetch(filename)
    dos2unix(filename)
    to_utf8(filename)


main()
