
import sys
from os.path import abspath, dirname, join
PREFIX = abspath(
    join(
        dirname(abspath(__file__)), '../../'
    )
)
if PREFIX not in sys.path:
    sys.path.append(PREFIX)

import z42.web.boot._env
