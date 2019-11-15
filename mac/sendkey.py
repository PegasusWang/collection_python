# -*- coding: utf-8 -*-

"""
使用 python 控制 mac 键盘
https://pypi.org/project/keyboard/
https://pythonhosted.org/pynput/keyboard.html

pip install pynput
"""

import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

time.sleep(3)
# Press and release space
keyboard.press('f')
keyboard.release('f')
time.sleep(0.5)
keyboard.press('s')
keyboard.release('s')
keyboard.press('w')
keyboard.release('w')

time.sleep(0.5)
keyboard.press('f')
keyboard.release('f')
time.sleep(0.5)
keyboard.press('d')
keyboard.release('d')
keyboard.press('w')
keyboard.release('w')

time.sleep(3) #删除时间久
keyboard.press('f')
keyboard.release('f')
time.sleep(1)
keyboard.press('s')
keyboard.release('s')
time.sleep(0.5)
keyboard.press('w')
keyboard.release('w')

#
# # Type a lower case A; this will work even if no key on the
# # physical keyboard is labelled 'A'
# Press and release space
# keyboard.press(Key.space)
# keyboard.release(Key.space)
# keyboard.press('a')
# keyboard.release('a')
#
# # Type two upper case As
# keyboard.press('A')
# keyboard.release('A')
# with keyboard.pressed(Key.shift):
#     keyboard.press('a')
#     keyboard.release('a')
#
# # Type 'Hello World' using the shortcut type method
# keyboard.type('Hello World')
