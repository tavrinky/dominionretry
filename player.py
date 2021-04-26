
from random import choice
from cards import * 

class Player(object): 
    def __init__(self, name): 
        self.name 
    
    def pickAction(self, g, pm): 
        print(f"Turn {g.turns}")
        actions = list(filter(lambda x: isinstance(x, Action), pm.hand)) 
        if actions and pm.actions: 
            return choice(actions) 
        else: 
            return None 

    def playTreasures(self, g, pm): 
        treasures = list(filter(lambda x: isinstance(x, Money), pm.hand)) 
        return treasures 

    def pickCardToBuy(self, g, pm): 
        print(g) 
        supplyCards = g.supply 
        supplyCardsByCost = [pile[0] for pile in supplyCards if pile] 
        print(supplyCardsByCost)
        #return max(filter(lambda x: x.cost <= pm.money, supplyCardsByCost), lambda x: x.cost) 
        
