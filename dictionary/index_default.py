#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""创建一个从单词到其出现情况的映射"""

import sys
import re
import collections
WORD_RE = re.compile(r'\w+')

index = collections.defaultdict(list)
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start()+1
            location = (line_no, column_no)
            index[word].append(location)
# 以字母顺序打印出结果
for word in sorted(index, key=str.upper):
    print(word, index[word])
