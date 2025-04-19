from tkinter import *
from tkinter import __all__ as tall

__all__ = tall

font_setting = None

def get_font(size:int, font:str = font_setting) -> tuple[str, int]:
    if font is None:
        raise ValueError('You are not set the defult font.')
    else:
        return (font, size)
    
def set_font(font:str):
    global font_setting

    font_setting = font