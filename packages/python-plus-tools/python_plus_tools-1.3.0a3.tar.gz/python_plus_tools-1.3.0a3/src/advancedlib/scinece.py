import pandas as pd
import pandas
import torch

from pathlib import Path
from os import getenv

from pyplus.tools import colors
from toml import load 

try:
    o1 = open(Path(getenv("appdata"),"xystudio", "pyplus", "config.toml"))
    o2 = open(Path(".xystudio", "pyplus", "config.toml").absolute())

    config = (load(o1) | load(o2)).get("library", {"showDeprecationWarning":True})['showDeprecationWarning']

    o1.close()
    o2.close()
except FileNotFoundError:
    config = True

if config:
    print(colors.Fore.YELLOW + colors.Style.BRIGHT + "DeprecationWarning: pyplus.science.science is deprecated since v1.2 and will be removed in v2.0. Please use pyplus.scince.pyscince (In 1.2.2 created)." + colors.Style.RESET_ALL)

del colors, load, getenv