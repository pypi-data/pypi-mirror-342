import operator

users = {}
user_level = {}

LEVEL = "level"
USER_NAME = "users"

if not __import__("os").path.exists(__import__("sys").prefix+"\\users") and __import__("os").path.isdir(__import__("sys").prefix+"\\users"): 
    if __import__("os").path.isdir(__import__("sys").prefix+"\\users"): 
        __import__("os").remove(__import__("sys").prefix+"\\users")
    __import__("os").mkdir(__import__("sys").prefix+"\\users")

def append(**kwargs): 
    """Add the users to users, if users in users, set the users."""
    for k, v in kwargs.items(): 
        users[k] = v

def get(key: str = None)->dict: 
    """get the keys users, if keys is none, return the users list, else return the key users`s value."""
    try: 
        return users[key]
    except: 
        raise NameError(key+" is not in users.")

def judge(useres, level): 
    try: 
        return users[useres] == level
    except Exception as e: 
        raise NameError(e)
    
def user_in_list(type, judge): 
    if type == LEVEL: 
        for k, v in users.items(): 
            if v == judge: 
                return True
        return False
    elif type ==  USER_NAME: 
        return judge in users
    else: 
        raise NameError(type+" is not in temp.")

def get_user(key: str = None)->dict: 
    """get the user users"""
    try: 
        return user_level[key]
    except: 
        raise NameError(key+" is not in users.")
    
def change_user(func, num, key: str = None)->dict: 
    """get the user users"""
    try: 
        user_level[key] = func(user_level[key], num)
        return user_level[key]
    except: 
        raise NameError(key+" is not in users.")
    
def del_user(key: str): 
    """delete the user keys."""
    try: 
        del user_level[key]
    except: 
        raise NameError(key+" is not in users.")

def set_user(**kwargs): 
    """Set the user Level"""
    for k, v in kwargs.items(): 
        user_level[k] = users[v]

def user_judge(type, judge): 
    if type == LEVEL: 
        for k, v in user_level.items(): 
            if users[k] == judge: 
                return True
        return False
    elif type ==  USER_NAME: 
        return judge in user_level
    else: 
        raise NameError(type+" is not in temp.")
    
def download(name): 
    import pickle

    with open(__import__("sys").prefix+"\\users\\" + name + ".jur", "rb") as f: 
        pickle.load(f)

def upload(name): 
    import pickle

    with open(__import__("sys").prefix+"\\users\\" + name + ".jur", "wb") as f: 
        pickle.dump([users, user_level], f)

set_permission = append
get_permission = get
judge_permission = judge

class User: 
    def __init__(self, name, level): 
        self.name = name
        self.level = level
    
    def change(self, do, value): 
        self.level = do(self.level, value)
        return self

    def operator(self, do, value): 
        if isinstance(value, User): 
            return do(self.level, value.level)
        elif isinstance(value, int): 
            return do(self.level, value)
        else: 
            raise TypeError("value '"+str(value)+"' is"+str(type(value))+", not User or int.")
    
    def __eq__(self, value : int): 
        return self.operator(operator.eq, value)

    def __ne__(self, value : int): 
        return self.operator(operator.ne, value)

    def __lt__(self, value : int): 
        return self.operator(operator.lt, value)

    def __gt__(self, value : int): 
        return self.operator(operator.gt, value)

    def __le__(self, value : int): 
        return self.operator(operator.le, value)

    def __ge__(self, value : int):     
        return self.operator(operator.ge, value)
    
    def __add__(self, value : int): 
        return self.change(operator.add, value)

    def __sub__(self, value : int): 
        return self.change(operator.sub, value)
    
    def __radd__(self, value : int): 
        return self.change(operator.add, value)

    def __rsub__(self, value : int): 
        return self.change(operator.sub, value)
    
    def __lshift__(self, value): 
        return self.change(operator.sub, value)
        
    def __rlshift__(self, value): 
        return self.change(operator.sub, value)

    def __rshift__(self, value): 
        return self.change(operator.add, value)
        
    def __rrshift__(self, value): 
        return self.change(operator.add, value)
