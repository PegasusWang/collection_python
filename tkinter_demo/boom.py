#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tkinter as tk
import random
import threading
import time


def boom():
    # 第1步，实例化object，建立窗口window
    window = tk.Tk()
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    a = random.randrange(0, width)
    b = random.randrange(0, height)
    # 第2步，给窗口的可视化起名字
    window.title("你是一个傻狍子")
    # 第3步，设定窗口的大小(长 * 宽)
    window.geometry('200x50')
    # 第4步，在图形界面上设定标签
    label = tk.Label(window,
                     text="你是一个傻狍子",
                     bg='green',
                     font=('宋体', 17),
                     width=a,
                     height=b)
    # 第5步，放置标签
    label.pack()
    # 第6步，主窗口循环显示
    window.mainloop()


if __name__ == '__main__':
    threads = []
    for i in range(5):
        t = threading.Thread(target=boom)
        threads.append(t)
        t.start()
        time.sleep(0.3)
    for t in threads:
        t.join()
