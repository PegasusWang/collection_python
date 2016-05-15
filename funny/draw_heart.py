#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
import math

text = open('heart.txt').read().replace(' ', '').replace('\n', '')
length = len(text)
limit = round(math.sqrt(length / (1.5 * math.pi)) / 8.8 * 15)

count = 0
for y in [-y  / limit / 0.66 for y in range(-limit, limit, 1)]:
    for x in [x / limit / 0.66 for x in range(-limit, limit, 1)]:
        if (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0:
            if count < length:
                sys.stdout.write(text[count])
                count = count + 1
            else:
                sys.stdout.write('**')
        else:
            sys.stdout.write('  ')
    sys.stdout.write('\n')

#print(text[count:-1])
