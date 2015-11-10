#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from noaho import NoAho    # 多模式匹配
from collections import Counter, defaultdict
trie = NoAho()
trie.add('hehe')
trie.add('py')
trie.add('python')


txt = """
我是谁不重要，重要的是你要学会python， hehe我是谁不重要，重要的是你要学会python
小米科技有限公司
"""

'''
c = defaultdict(int)
words = [txt[k[0]:k[1]] for k in trie.findall_long(txt)]
wc = Counter(words)

for k in trie.findall_long(txt):
    word = txt[k[0]:k[1]]
    c[word] += 1
    #print(k)
    print(txt[k[0]:k[1]])


for k, v in wc.items():
    print k, v
'''
k = trie.find_short(txt)
print(txt[k[0]:k[1]])

print('************')

k = trie.find_long(txt)
print(txt[k[0]:k[1]])


print('************')
k_all = trie.findall_short(txt)
for k in k_all:
    print(txt[k[0]:k[1]])

print('************')
k_all = trie.findall_long(txt)
for k in k_all:
    print(txt[k[0]:k[1]])
