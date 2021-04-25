
from random import choice
from cards import * 

class Player(object): 
    def __init__(self): 
        pass 
    
    def pickAction(self, g, pm): 
        actions = list(filter(lambda x: isinstance(x, Action), pm.hand)) 
        if actions and pm.actions: 
            return choice(actions) 
        else: 
            return None 
