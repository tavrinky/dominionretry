
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

class Curse(Card): 
    def __init__(self): 
        super().__init__(0)

    def setupSupply(self, _): 
        return [self.__class__() for _ in range(10)] 




