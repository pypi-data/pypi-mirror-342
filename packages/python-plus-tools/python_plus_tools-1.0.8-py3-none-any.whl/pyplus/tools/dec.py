from .update import *
from .update import upload

__all__=["ALL", "NEW", "WILL", 
        "get_update", "get_version_update_time", "get_news_update_time", "get_new", "get_all", "get_will", 
        "get_pre_update", "get_pre_version_update_time", "get_pre_news_update_time", "get_pre_news_update_time", "get_pre_new", "get_pre_all"]

class dint(int):
    pass

class istr(str):
    pass
