#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""打印ASCII字母表、数字、标点符号"""
import string

for item in [string.ascii_letters,string.digits,string.punctuation]:
    print(f"{len(item)}\t{item}")
