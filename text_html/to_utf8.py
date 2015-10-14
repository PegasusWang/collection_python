#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


def get_all_htm(path):
    res = set()
    list_dirs = os.walk(path)
    for root, dirs, files in list_dirs:
        for f in files:
            if f.endswith('.htm'):
                res.add(os.path.join(root, f))
    return res


'''
请注意 gb2312 不是 “gb2312”，凡 gb2312 的请换成 gb18030.
微软将 gb2312 和 gbk 映射为 gb18030，方便了一些人，也迷惑了一些人。
'''
def to_utf8(filename):
    lines = open(filename, 'r').readlines()
    lines = [i.replace('\r\n', '\n').strip() for i in lines]
    for i, line in enumerate(lines):
        if 'utf-8' in line:
            lines[i] = ''
            continue
        if 'charset=gb2312' in line:
            lines[i] = line.replace('charset=gb2312', 'charset=utf-8')
            continue
        elif 'charset=gbk' in line:
            lines[i] = line.replace('charset=gbk', 'charset=utf-8')

    txt = '\n'.join(lines)
    content = txt.decode('gb18030').encode('utf-8')
    filename += 'l'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    htm_files = get_all_htm('.')
    for f in htm_files:
        print(f)
        to_utf8(f)


if __name__ == '__main__':
    main()
