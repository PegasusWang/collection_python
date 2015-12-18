import _env
from z42.config import DISABLE_LOCAL_CACHED
from z42.config import MC_CONFIG
import pylibmc
mc = pylibmc.Client(MC_CONFIG)

from mc_connection import init_mc
mc = init_mc(mc, DISABLE_LOCAL_CACHED)
