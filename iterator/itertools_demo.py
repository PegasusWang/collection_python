#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import dropwhile, islice, permutations, combinations

with open('demo.txt', 'r', encoding='utf-8') as file:
    # 按照真值函数丢弃掉列表和迭代器前面的元素
    for line in dropwhile(lambda line: line.startswith('#'), file):
        print(line, end='')

for line in dropwhile(lambda e: e < 5, range(10)):
    print(line, end='')
print()

items = ['a', 'b', 'c', 1, 4, 10, 15]
# 对迭代器进行切片
for x in islice(items, 3, None):
    print(x)

items = ['a', 'b', 'c']
# 产生指定数目的元素的所有排列(顺序有关)
for p in permutations(items):
    print(p)

for p in permutations(items, 2):
    print(p)

# 求列表或生成器中指定数目的元素不重复的所有组合
for c in combinations(items, 3):
    print(c)

for c in combinations(items, 2):
    print(c)
