
from utils import * 

class Card(object): 
    def __init__(self, cost): 
        self.cost = cost

    def __eq__(self, other): 
        return self.__class__ == other.__class__ 

    def __str__(self):
        return super().__str__().split(".")[1].split(" ")[0]

    def __hash__(self):
        return hash(str(self))

class Money(Card): 
    def __init__(self, cost, value): 
        super().__init__(cost) 
        self.value = value 

class Copper(Money): 
    def __init__(self): 
        super().__init__(0, 1) 

    def setupSupply(self, numPlayers): 
        return [Copper() for _ in range(60-(7*numPlayers))] 

class Silver(Money): 
    def __init__(self): 
        super().__init__(3, 2) 
    
    def setupSupply(self, _):
        return [Silver() for _ in range(40)] 

class Gold(Money): 
    def __init__(self): 
        super().__init__(6, 3) 

    def setupSupply(self, _): 
        return [Gold() for _ in range(30)] 

class Victory(Card): 
    def __init__(self, cost, vp): 
        super().__init__(cost) 
        self.vp = vp 

    def getVP(self, game): 
        return self.vp(game) 

    def setupSupply(self, numPlayers): 
        if numPlayers < 3: 
            numCards = 8 
        else: 
            numCards = 12 
        return [self.__class__() for _ in range(numCards)] 

class Estate(Victory): 
    def __init__(self): 
        super().__init__(2, lambda _: 1)

class Duchy(Victory): 
    def __init__(self): 
        super().__init__(5, lambda _: 3)

class Province(Victory): 
    def __init__(self): 
        super().__init__(8, lambda _: 6)

class Action(Card): 
    def __init__(self, cost): 
        super().__init__(cost) 

    def setupSupply(self, _): 
        return [self.__class__() for _ in range(10)] 

class Village(Action): 
    def __init__(self): 
        super().__init__(3) 

    def run(self, g): 
        g.currentPM.actions += 2 
        g.currentPM.draw() 

class Smithy(Action): 
    def __init__(self): 
        super().__init__(4) 

    def run(self, g): 
        g.currentPM.drawN(3) 

class Chapel(Action): 
    def __init__(self): 
        super().__init__(2) 

    def run(self, g): 
        cardsToTrash = g.currentPlayer.chapel(g.viewGame(), g.currentPM.viewPM()) 
        for card in cardsToTrash: 
            if card not in g.currentPM.hand: 
                raise ValueError(f"Tried to trash card not in hand! Card: {card}, hand: {g.currentPM.hand}") 
            else: 
                g.currentPM.hand.remove(card) 
                g.trashCard(card) 

class Cellar(Action): 
    def __init__(self): 
        super().__init__(2) 

    def run(self, g): 
        cardsToCellar = g.currentPlayer.cellar(g.viewGame(), g.currentPM.viewPM()) 
        for card in cardsToCellar: 
            if card not in g.currentPM.hand: 
                raise ValueError(f"Tried to cellar card not in hand! Card: {card}, hand: {g.currentPM.hand}") 
            else: 
                g.currentPM.discardCard(card) 
                g.currentPM.draw() 

# skipping moat because what the fuck is a reaction 

class Harbinger(Action): 
    def __init__(self): 
        super().__init__(3) 

    def run(self, g): 
        g.currentPM.draw() 
        g.currentPM.actions += 1 
        cardToHarbinger = g.currentPlayer.harbinger(g.viewGame(), g.currentPM.viewPM()) 
        if g.currentPM.discard: 
            if cardToHarbinger in g.currentPM.discard: 
                g.currentPM.discard.remove(cardToHarbinger) 
                g.currentPM.hand.append(cardToHarbinger) 
            else: 
                return ValueError(f"Tried to harbinger card not in discard: Card {Card}, hand: {g.currentPM.hand}")  
        else: 
            pass


class Merchant(Action): 
    def __init__(self): 
        super().__init__(3) 

    def run(self, g): 
        def merchantBuyHandler(g, card, t=Triggered()): 
            if not t.triggered and isinstance(card, Silver): 
                g.currentPM.money+=1 
                t.trigger() 
            
        g.currentPM.draw() 
        g.currentPM.actions += 1 
        g.attachOnPlayTreasureHandler(merchantBuyHandler)

class Vassal(Action): 
    def __init__(self): 
        super().__init__(3) 

    def run(self, g): 
        g.currentPM.money += 2 
        cardToVassal = g.currentPM.deck.pop(0) 
        if isinstance(cardToVassal, Action) and g.currentPlayer.vassal(g.viewGame(), g.currentPM.viewPM(), cardToVassal): 
            g.inPlay.append(cardToVassal) 
            cardToVassal.run(g)
        else: 
            g.currentPM.discard.append(cardToVassal)

class Workshop(Action): 
    def __init__(self): 
        super().__init__(3)

    def run(self, g): 
        cardToWorkshop = g.currentPlayer.workshop(g.viewGame(), g.currentPM.viewPM()) 
        pile = g.getSupplyByName(cardToWorkshop.__class__)
        if pile: 
            g.currentPM.discard.append(pile.pop(0)) 
            


class Curse(Card): 
    def __init__(self): 
        super().__init__(0)

    def setupSupply(self, _): 
        return [self.__class__() for _ in range(10)] 






