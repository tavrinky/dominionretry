from random import shuffle, choice 

from player import Player 
from cards import * 
from utils import random_string
from log import PrintLog

class Game(object):
    def __init__(self, numplayers=2): 
        players = [Player(str(i)) for i in range(numplayers)]
        self.trash = [] 
        self.supply = [] 
        self.playermanagers = [PlayerManager(player) for player in players] 
        cardsInSupply = [ 
            Estate, 
            Duchy, 
            Province, 
            Copper,
            Silver, 
            Gold, 
            Village,
            Curse,
        ]

        self.log = PrintLog() 
        self.setupSupply(*cardsInSupply)
        
        [pm.setup() for pm in self.playermanagers]   
        self.turn = 0 
        self.currentPlayer = [pm.player for pm in self.playermanagers][0]

        

    def setupSupply(self, *cards):
        self.log.log("Setting up")
        numPlayers = len(self.playermanagers)
        for card in cards: 
            self.supply.append(card().setupSupply(numPlayers))

    @property 
    def currentPM(self): 
        for p in self.playermanagers: 
            if p.player == self.currentPlayer: 
                return p 
        raise AssertionError("Every player in the game should have a player manager")

    def getSupplyByName(self, cardName): 
        for pile in self.supply: 
            if cardName() in pile: 
                return pile 

    def run(self): 
        self.log.log(f"Beginning turn {self.turn}, {self.currentPlayer.name}'s turn")
        while not self.isWon(): 
            self.stepTurn()

    def stepTurn(self): 
        for pm in self.playermanagers: 
            assert(len(pm.hand)==5 )
        self.currentPM.actions, self.currentPM.buys = 1,1 
        self.currentPM.money = 0 
        self.log.log("Beginning actions") 
        self.runActions() 
        self.log.log("Beginning buys") 
        self.runBuys()
        self.log.log("Cleaning up")
        self.cleanUp() 
        self.incrementPlayer() 

    def isWon(self): 
        return self.threePiled() or self.provincesEmpty() 

    def threePiled(self): 
        numEmpty = 0 
        for pile in self.supply: 
            if not pile: 
                numEmpty += 1 
        return numEmpty >= 3 

    def provincesEmpty(self): 
        return not self.getSupplyByName(Province)
        
    def runActions(self): 
        while self.currentPM.actions > 0:  
            action = self.currentPlayer.pickAction(viewGame(self), viewPM(self.currentPM)) 
            if action in self.currentPM.hand: 
                self.currentPM.discardCard(action) 
                self.currentPM.actions -= 1 
                action.run(self) 
            if not action: 
                break 

    def runBuys(self):
        treasures = self.currentPlayer.playTreasures(viewGame(self), viewPM(self.currentPM))
        
        for treasure in treasures:      
            if treasure in self.currentPM.hand and isinstance(treasure, Money): 
                self.currentPM.discardCard(treasure) 
                self.currentPM.money += treasure.value 
            else: 
                raise ValueError("Bad and naughty player, playing treasures you don't have!\nHand: {self.currentPM.hand}, treasure: {treasure}")
        while self.currentPM.buys > 0: 
            cardToBuy = self.currentPlayer.pickCardToBuy(viewGame(self), viewPM(self.currentPM)) 
            if cardToBuy and cardToBuy.cost <= self.currentPM.money: 
                self.currentPM.buys -= 1 
                self.currentPM.discard.append(self.getSupplyByName(cardToBuy.__class__).pop(0))
            elif not cardToBuy: 
                break 
            else: 
                raise ValueError("Tried to buy card that costs too much, money: {self.currentPM.money}, {cardToBuy}") 

    def cleanUp(self): 
        self.currentPM.discardHand() 
        self.currentPM.drawN(5) 
        assert(len(self.currentPM.hand) == 5 )

    def incrementPlayer(self): 
        # assumptions: every player has a player manager
        # every player manager has a player 
        # I think this works if you have [p1, p2] and [pm2, pm1] where pmn.player = pn 
        players = [pm.player for pm in self.playermanagers]  
        currentIndex = players.index(self.currentPlayer) 
        currentIndex += 1 
        self.currentPlayer = players[currentIndex % len(players)] 

    def printSupply(self): 
        for pile in self.supply: 
            if pile: 
                self.log.log(f"{len(pile)} {str(pile[0])}s")
        
# basically just a glorified tuple 
class PlayerVisibleGame(object): 
    def __init__(self, trash, supply, turn): 
        print(trash)
        self.trash = trash
        self.supply = supply 
        self.turn = turn

def viewGame(g): 
    return PlayerVisibleGame(trash=g.trash[:], supply=g.supply[:][:], turn=g.turn)
    
class PlayerManager(object): 
    def __init__(self, player): 
        self.player = player 
        self.deck = [] 
        self.discard = [] 
        self.hand = [] 
        self.actions = 0 
        self.money = 0 
        self.buys = 0 
        
    def setup(self): 
        self.deck += [Copper() for _ in range(7)] 
        self.deck += [Estate() for _ in range(3)] 
        shuffle(self.deck) 
        self.drawN(5)

    def discardHand(self): 
        self.discard += self.hand 
        self.hand = [] 

    def draw(self): 
        if self.deck: 
            self.hand.append(self.deck.pop(0)) 
        else: 
            self.deck = self.discard[:]
            shuffle(self.deck) 
            self.discard = [] 
            self.hand.append(self.deck.pop(0))
            
    
    def drawN(self, n): 
        [self.draw() for _ in range(n)]

    def viewHand(self, player): 
        if player == self.player: 
            return self.hand 
        else: 
            # TODO: fix for attacks 
            pass 

    def discardCard(self, card): 
        self.hand.remove(card)
        self.discard.append(card) 

    
class ViewablePlayerManager(object):
    def __init__(self, actions, money, buys, deck, discard, hand): 
        self.actions = actions 
        self.money = money 
        self.buys = buys 
        self.deck = deck[:]
        shuffle(self.deck)
        self.discard = discard[:]
        self.hand = hand[:]

def viewPM(pm): 
    pmDict = {
        "actions": pm.actions,
        "money": pm.money,
        "buys": pm.buys,
        "deck": pm.deck,
        "discard": pm.discard, 
        "hand": pm.hand,
    }
    return ViewablePlayerManager(**pmDict)

if __name__ == "__main__": 
    game = Game()
    game.run()