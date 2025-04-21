from typing import TypeVar

T = TypeVar('T')




class Failure:
    def __init__(self, data: T)-> None:
        self.data= data

class Ok:
    def __init__(self, data: T)-> None:
        self.data= data
    
