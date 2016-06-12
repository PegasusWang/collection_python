#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Fore.GREEN+ 'some red text')
pprint(Fore.GREEN+ str(dict(a=1,b=2)))

"""
Fore.BLACK            Fore.LIGHTBLACK_EX    Fore.LIGHTMAGENTA_EX  Fore.MAGENTA          Fore.YELLOW
Fore.BLUE             Fore.LIGHTBLUE_EX     Fore.LIGHTRED_EX      Fore.RED
Fore.CYAN             Fore.LIGHTCYAN_EX     Fore.LIGHTWHITE_EX    Fore.RESET
Fore.GREEN            Fore.LIGHTGREEN_EX    Fore.LIGHTYELLOW_EX   Fore.WHITE
"""
