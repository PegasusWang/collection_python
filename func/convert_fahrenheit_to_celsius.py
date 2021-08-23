#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
提示：华氏温度到摄氏温度的转换公式为：$C=(F - 32) \div 1.8$。
"""


def convert_temperature(temperature):
    """
    华氏温度到摄氏温度的转换
    """
    try:
        fahrenheit = float(temperature)
    except Exception as err:
        print(err)
    else:
        celsius = (fahrenheit - 32) / 1.8
        return celsius


if __name__ == '__main__':
    f = 100
    c = convert_temperature(f)
    print('%.1f华氏度 = %.1f摄氏度' % (f, c))
