# -*- coding: utf-8 -*-

"""生成 ascii 字体
pip install colorama termcolor pyfiglet

"""

import sys

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

# cprint(figlet_format('missile!', font='starwars'), 'yellow', 'on_red', attrs=['bold'])
# cprint(figlet_format(u'docker vim'))
# cprint(figlet_format(u'Python/Go Web Guide'))
cprint(figlet_format(u'Python/Go Web Guide', width=300))

"""

    ____        _   _                  __        __   _          ____       _     _
|  _ \ _   _| |_| |__   ___  _ __   \ \      / /__| |__      / ___|_   _(_) __| | ___
| |_) | | | | __| '_ \ / _ \| '_ \   \ \ /\ / / _ \ '_ \    | |  _| | | | |/ _` |/ _ \
|  __/| |_| | |_| | | | (_) | | | |   \ V  V /  __/ |_) |   | |_| | |_| | | (_| |  __/
|_|    \__, |\__|_| |_|\___/|_| |_|    \_/\_/ \___|_.__/     \____|\__,_|_|\__,_|\___|
        |___/

"""
