from builtins import abs as _abs

def select(a:object, b:object ,select: bool) -> object:
    '''
    Select a value.

    :example: 
    >>> import pyplus
    >>> pyplus.tools.dec.select(1, 2, False)
    >>> 1
    >>> pyplus.tools.dec.select(1, 2, True)
    >>> 2
    
    :param bool select: If select == True,return b, else return a.
    :param object a: If select == False,return a.
    :param object b: If select == True,return b.

    :return object: If select == True,return b, else return a.
    '''
    return b if select else a

def space(a, b) -> int:
    '''
    :example: 
    >>> import pyplus
    >>> pyplus.tools.dec.space(1, 2)
    >>> -1
    >>> pyplus.tools.dec.select(2, 2)
    >>> 0
    >>> pyplus.tools.dec.select(3, 2)
    >>> 1

    :return int: 
    If a < b,return -1.
    If a > b,return 1.
    If a == b,return 0.
    '''
    return (a > b) - (a < b)

def abs(a):
    "Same as abs(a)."
    return _abs(a)

def add(a, b):
    "Same as a + b."
    return a + b

def and_(a, b):
    "Same as a & b."
    return a & b

def floordiv(a, b):
    "Same as a // b."
    return a // b

def index(a):
    "Same as a.__index__()."
    return a.__index__()

def inv(a):
    "Same as ~a."
    return ~a
invert = inv

def lshift(a, b):
    "Same as a << b."
    return a << b

def mod(a, b):
    "Same as a % b."
    return a % b

def mul(a, b):
    "Same as a * b."
    return a * b

def matmul(a, b):
    "Same as a @ b."
    return a @ b

def neg(a):
    "Same as -a."
    return -a

def or_(a, b):
    "Same as a | b."
    return a | b

def pos(a):
    "Same as +a."
    return +a

def pow(a, b):
    "Same as a ** b."
    return a ** b

def rshift(a, b):
    "Same as a >> b."
    return a >> b

def sub(a, b):
    "Same as a - b."
    return a - b

def truediv(a, b):
    "Same as a / b."
    return a / b

def xor(a, b):
    "Same as a ^ b."
    return a ^ b