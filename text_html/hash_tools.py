#!/usr/bin/env python
# -*- coding:utf-8 -*-


def file_md5(filepath, chunksize=4096):
    import hashlib
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(chunksize), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


if __name__ == "__main__":
    print(file_md5('./common.txt'))
