from modulelib import *

from os import getenv
from pathlib import Path

from pyplus.tools import colors
from toml import load 

try:
    o1 = open(Path(getenv("appdata"),"xystudio", "pyplus", "config.toml"))
    o2 = open(Path(".xystudio", "pyplus", "config.toml").absolute())

    config = (load(o1) | load(o2)).get("library", {"showDeprecationWarning" : True}).get("showDeprecationWarning", True)
    o1.close()
    o2.close()
except FileNotFoundError:
    config = True

if config:
    print(colors.Fore.YELLOW + "DeprecationWarning: pyplus.tools.moudle is deprecated since v1.3 and will be removed in v2.0. Please use modulelib." + colors.Style.RESET_ALL)

del colors, load, getenv, Path