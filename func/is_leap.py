#!/usr/bin/env python
# -*- coding:utf-8 -*-

def is_leap(year):
    """
    输入年份 如果是闰年输出True 否则输出False
    """
    try:
        year = int(year)
    except Exception as err:
        print(err)
    else:
        is_leap = year % 4 == 0 and year % 100 != 0 or \
                  year % 400 == 0
        return is_leap


if __name__ == '__main__':
    year = input('请输入年份: ')
    res = is_leap(year)
    print(f'{year} 是否闰年：{res}')
