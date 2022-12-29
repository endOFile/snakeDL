import numpy as np

actions = []

#può essere anche una funzione
#rewards = np.array([[],[]])

class QAgent():

    def __init__(self, alpha, gamma, states, actions) -> None:
        self.gamma = gamma
        self.alpha = alpha
        self.actions = actions
        self.states = states
    
    def training(self, iterations):