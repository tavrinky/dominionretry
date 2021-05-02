
from random import choice
from cards import * 

class Player(object): 
    def __init__(self, name): 
        self.name = name 
    
    def pickAction(self, g, pm): 
        
        actions = list(filter(lambda x: isinstance(x, Action), pm.hand)) 
        if actions and pm.actions: 
            return choice(actions) 
        else: 
            return None 

    def playTreasures(self, g, pm): 
        treasures = list(filter(lambda x: isinstance(x, Money), pm.hand)) 
        return treasures 

    def pickCardToBuy(self, g, pm): 
        supplyCards = g.supply 
        supplyCardsByCost = [pile[0] for pile in supplyCards if pile] 
        # cursed 
        cards = [card for card in supplyCardsByCost if card.cost <= pm.money] 
        if cards: 
            card = max(cards, key=lambda x: x.cost)
            print(card)
            return card 
        else: 
            return None 

    def chapel(self, g, pm): 
        return [x for x in pm.hand if isinstance(x, Estate)]

    def cellar(self, g, pm): 
        return [x for x in pm.hand if isinstance(x, Victory)]

    def harbinger(self, g, pm): 
        if pm.discard: 
            return max(pm.discard, key=lambda x: x.cost) 
        else: 
            return None 
        
        
