from queue import Queue, SimpleQueue
from collections import deque

class FIFOStack:
    def __init__(self):
        self.stacks = []

    def put(self, items):
        self.stacks.append(items)

    def push(self):
        return self.stacks.pop(0)
    
    def get(self):
        return self.push()
    
    @property
    def is_empty(self):
        return len(self.stacks) == 0
    
    def __sizeof__(self):
        return len(self)
        
    def __len__(self):
        return len(self.stacks)
    
    def __repr__(self):
        return f"Stack({",".join(self.stacks)})"
    
    def  __str__(self):
        return self.__repr__()
    
    def __add__(self, value):
        out_list = self.stacks.append(value)
        o = FIFOStack()
        o.stacks = out_list
        return o

class ThreadFIFOStack(Queue):
    def push(self, items):
        self.stacks.append(items)
    
    def __sizeof__(self):
        return len(self)
        
    def __len__(self):
        return len(self.stacks)
    
    def __repr__(self):
        return f"Stack({",".join(self.stacks)})"

    def  __str__(self):
        return self.__repr__()

class LIFOStack:
    def __init__(self):
        self.stacks = []

    def put(self, items):
        self.stacks.append(items)

    def push(self):
        return self.stacks.pop()
    
    def get(self):
        return self.push()
    
    @property
    def is_empty(self):
        return len(self.stacks) == 0
    
    def __sizeof__(self):
        return len(self)
        
    def __len__(self):
        return len(self.stacks)
    
    def __repr__(self):
        return f"Stack({",".join(self.stacks)})"
    
    def  __str__(self):
        return self.__repr__()
    
    def __add__(self, value):
        out_list = self.stacks.append(value)
        o = FIFOStack()
        o.stacks = out_list
        return o
