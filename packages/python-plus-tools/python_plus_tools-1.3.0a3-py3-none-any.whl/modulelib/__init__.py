from importlib import *

def get_import_moudle_path():
    from sys import modules
    if __name__ != "__main__":
        main_moudle = modules['__main__']
        if hasattr(main_moudle, '__file__'):
            return main_moudle.__file__
        else:
            return None