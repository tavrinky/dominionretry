
from random import choice
from cards import * 

from typing import List, Optional, TYPE_CHECKING
if TYPE_CHECKING: 
    from game import * 
class Player(object): 
    def __init__(self, name: str): 
        self.name = name 
    
    def pickAction(self, g: Game, pm : PlayerManager) -> Optional[Action]: 
        
        actions = list(filter(lambda x: isinstance(x, Action), pm.hand)) 
        if actions and pm.actions: 
            return choice(actions) 
        else: 
            return None 

    def playTreasures(self, g: Game, pm: PlayerManager) -> List[Money]: 
        treasures = list(filter(lambda x: isinstance(x, Money), pm.hand)) 
        return treasures 

    def pickCardToBuy(self, g: Game, pm: PlayerManager) -> Optional[Card]: 
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

    def chapel(self, g: Game, pm: PlayerManager) -> List[Card]: 
        return [x for x in pm.hand if isinstance(x, Estate)]

    def cellar(self, g: Game, pm: PlayerManager) -> List[Card]: 
        return [x for x in pm.hand if isinstance(x, Victory)]

    def harbinger(self, g: Game, pm: PlayerManager) -> Optional[Card]: 
        if pm.discard: 
            return max(pm.discard, key=lambda x: x.cost) 
        else: 
            return None 

    def vassal(self, g: Game, pm: PlayerManager, card: Card) -> bool: 
        return True 

    def workshop(self, g: Game, pm: PlayerManager) -> Card: 
        return Silver() 

    def revealed(self, g: Game, cards: List[Card], message: str): 
        pass 

    def respondToBureaucrat(self, g: Game, pm: PlayerManager, cards: List[Card]) -> Optional[Card]: 
        if cards: 
            return cards[0] 
        #gnashes my teeth while reciting the zen of python 
        return None 
        
