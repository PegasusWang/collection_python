# coding=utf-8

import sys
import os
import hashlib
from functools import partial


def get_file_md5(f, chunk_size=8192):
    h = hashlib.md5()
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdigest()


def humanize_bytes(bytesize, precision=2):
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return '%.*f %s' % (precision, bytesize / factor, suffix)


def python_obj_size(obj, humanize=True):
    """ 获取一个python对象的大小，默认返回人可读的形式 """
    if humanize:
        return humanize_bytes(sys.getsizeof(obj))
    else:
        return sys.getsizeof(obj)


if __name__ == "__main__":
    print(humanize_bytes(1024*1024))
