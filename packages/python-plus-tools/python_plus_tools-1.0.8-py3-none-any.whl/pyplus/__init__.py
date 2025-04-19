'''
The python Plus - Pyplus
================
the python's plus library.\n
'''

from .tools.update import *
from .tools.update import get_update_from_toml
from . import science ,tools
from site import getsitepackages

__all__=["science" ,"tools" ,
         "ALL" ,"NEW" ,"WILL" ,
         "get_update" ,"get_version_update_time" ,"get_news_update_time" ,"get_new" ,"get_all" ,"get_will" ,"get_version",
        ]

get_update_from_toml("pyplus\\update.toml",code_name="main")
