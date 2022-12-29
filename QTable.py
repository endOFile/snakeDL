class QTable():

    lRate = .95
    dRate = .75

    # 1 = cella occupata
    # 0 = cella libera
    IND_UP = 0
    IND_RIGHT = 1
    IND_DOWN = 2
    IND_LEFT = 3

    # -1 mela a sinistra / sopra
    #  0 mela nella stessa colonna / riga
    # +1 mela a destra / sotto 
    IND_POS_FOOD_H = 4
    IND_POS_FOOD_V = 5

    IND_ACTION_UP = 0
    IND_ACTION_RIGHT = 1
    IND_ACTION_DOWN = 2
    IND_ACTION_LEFT = 3
    
    def __init__(self):
        self.table = dict()
        for i in range(0, 2):
            for j in range(0, 2):
                for k in range(0, 2):
                    for l in range(0, 2):
                        for m in range(-1, 2):
                            for n in range(-1, 2):
                                self.table[str(i)+str(j)+str(k)+str(l)+str(m)+str(n)] = [0,0,0,0]

    def chooseAction(self, state):
        return self.table[state].index(max(self.table[state]))

    def updateTable(self, state, action, reward, futureReward):
        oldQ = self.table[state][action]
        self.table[state][action] = oldQ + self.lRate * (reward + self.dRate * (futureReward) - oldQ)