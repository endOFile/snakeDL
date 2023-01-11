import random as rd

class QTable():

    lRate = .001
    dRate = .05
    EXP_STEP = .1
    MIN_EXPLORATION = .001

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
                                self.table[str(i)+str(j)+str(k)+str(l)+str(m)+str(n)] = [[0,0,0,0], .9]

    def chooseAction(self, state, enabExplor):
        if enabExplor and rd.random() <= self.table[state][1]:
            temp_exp = self.table[state][1]-self.EXP_STEP
            self.table[state][1] = (self.MIN_EXPLORATION if temp_exp < self.MIN_EXPLORATION else temp_exp)
            return rd.randint(0,3)
        return self.table[state][0].index(max(self.table[state][0]))

    def maxAction(self, state):
        return max(self.table[state][0])

    def updateTable(self, state, action, reward, next_state):
        old_q = self.table[state][0][action]
        next_q = self.maxAction(next_state)
        self.table[state][0][action] = old_q + self.lRate * (reward + self.dRate * next_q - old_q)

    def printTable(self):
        print(self.table)