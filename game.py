from random import shuffle, choice 

from player import Player 
from cards import * 
from utils import random_string
from log import * 

from typing import Callable, Optional, Type 

class Game(object):
    def __init__(self, numplayers: int =2): 
        players: List[Player] = [Player(str(i)) for i in range(numplayers)]
        self.trash: List[Card] = [] 
        self.supply: List[List[Card]] = [] 
        self.inPlay: List[Card] = [] 
        self.playermanagers: List[PlayerManager] = [PlayerManager(player) for player in players] 
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

        self.log: Log = PrintLog() 
        self.setupSupply(*cardsInSupply)

        self.onPlayTreasureHandlers: List[Callable] = [] 
        
        [pm.setup() for pm in self.playermanagers]   
        self.turn: int = 0 
        self.currentPlayer: Player = [pm.player for pm in self.playermanagers][0]

        

    def setupSupply(self, *cards: List[Type[Card]]):
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
        self.currentPM.actions, self.currentPM.buys = 1,1 
        self.currentPM.money = 0 
        self.log.log("Beginning actions") 
        self.runActions() 
        self.log.log("Beginning buys") 
        self.runBuys()
        self.log.log("Cleaning up")
        self.cleanUp() 
        self.incrementPlayer() 

    def isWon(self) -> bool: 
        return self.threePiled() or self.provincesEmpty() 

    def threePiled(self) -> bool: 
        numEmpty = 0 
        for pile in self.supply: 
            if not pile: 
                numEmpty += 1 
        return numEmpty >= 3 

    def provincesEmpty(self) -> bool: 
        return not self.getSupplyByName(Province)
        
    def runActions(self): 
        while self.currentPM.actions > 0:  
            action = self.currentPlayer.pickAction(viewGame(self), viewPM(self.currentPM)) 
            if action in self.currentPM.hand: 
                self.currentPM.hand.remove(action) 
                self.inPlay.append(action) 
                self.currentPM.actions -= 1 
                action.run(self) 
                if isinstance(action, Attack): 
                    action.attack(self) 
            if not action: 
                break 

    def runBuys(self):
        treasures: List[Money] = self.currentPlayer.playTreasures(viewGame(self), viewPM(self.currentPM))
        for treasure in treasures:      
            if treasure in self.currentPM.hand and isinstance(treasure, Money): 
                self.currentPM.hand.remove(treasure)  
                self.inPlay.append(treasure) 
                self.currentPM.money += treasure.value 
                for h in self.onPlayTreasureHandlers: 
                    h(self, treasure)
            else: 
                raise ValueError("Bad and naughty player, playing treasures you don't have!\nHand: {self.currentPM.hand}, treasure: {treasure}")
        while self.currentPM.buys > 0: 
            cardToBuy: Optional[Card] = self.currentPlayer.pickCardToBuy(viewGame(self), viewPM(self.currentPM)) 
            if cardToBuy and cardToBuy.cost <= self.currentPM.money: 
                self.currentPM.buys -= 1 
                self.currentPM.money -= cardToBuy 
                self.currentPM.discard.append(self.getSupplyByName(cardToBuy.__class__).pop(0))
            elif not cardToBuy: 
                break 
            else: 
                raise ValueError("Tried to buy card that costs too much, money: {self.currentPM.money}, {cardToBuy}") 
        self.onPlayTreasureHandlers: List[Callable] = [] 

    def cleanUp(self): 
        self.currentPM.discardHand() 
        self.currentPM.discard.extend(self.inPlay) 
        self.inPlay: List[Card] = [] 
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

    def trashCard(self, card): 
        self.trash.append(card)

    # put here so that i don't need to import it into cards 
    def viewGame(self): 
        return viewGame(self) 

    def attachOnPlayTreasureHandler(self, handler): 
        self.onPlayTreasureHandlers.append(handler) 

    def reveal(self, cards, message): 
        for player in map(lambda pm: pm.player, self.playermanagers): 
            player.revealed(self.viewGame(), cards, message)
        
            
        
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

    def viewPM(self): 
        return viewPM(self)  




    
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
    game.currentPM.hand.append(Chapel()) 
    game.run()