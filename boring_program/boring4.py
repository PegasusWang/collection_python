#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tkinter as tk
import random
import threading
import time

#
# from:https://mp.weixin.qq.com/s/R9Z0LR9htZcgl7vVvY1sdQ
# 这个程序就动感多了，会随机出现弹窗。
# 运行效果如下图所示，非常带劲，可以任意修改。

def boom():
    window = tk.Tk()
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    a = random.randrange(0, width)
    b = random.randrange(0, height)
    window.title('你是一个傻狍子')
    window.geometry("200x50" + "+" + str(a) + "+" + str(b))
    tk.Label(window, text='你是一个傻狍子', bg='green',
             font=('宋体', 17), width=20, height=4).pack()
    window.mainloop()


threads = []
for i in range(100):
    t = threading.Thread(target=boom)
    threads.append(t)
    time.sleep(0.1)
    threads[i].start()
