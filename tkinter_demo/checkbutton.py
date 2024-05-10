#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tkinter as tk  # 使用Tkinter前需要先导入

# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('My Window')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x

# 第4步，在图形界面上创建一个标签label用以显示并放置
l = tk.Label(window, bg='yellow', width=20, text='empty')
l.pack()


# 第6步，定义触发函数功能
def print_selection():
    if (var1.get() == 1) & (var2.get() == 0):  # 如果选中第一个选项，未选中第二个选项
        l.config(text='I love only Python ')
    elif (var1.get() == 0) & (var2.get() == 1):  # 如果选中第二个选项，未选中第一个选项
        l.config(text='I love only C++')
    elif (var1.get() == 0) & (var2.get() == 0):  # 如果两个选项都未选中
        l.config(text='I do not love either')
    else:
        l.config(text='I love both')  # 如果两个选项都选中


# 第5步，定义两个Checkbutton选项并放置
var1 = tk.IntVar()  # 定义var1和var2整型变量用来存放选择行为返回值
var2 = tk.IntVar()
c1 = tk.Checkbutton(window, text='Python', variable=var1, onvalue=1, offvalue=0,
                    command=print_selection)  # 传值原理类似于radiobutton部件
c1.pack()
c2 = tk.Checkbutton(window, text='C++', variable=var2, onvalue=1, offvalue=0, command=print_selection)
c2.pack()

# 第7步，主窗口循环显示
window.mainloop()
