from __future__ import annotations

import random
from player import Player
from dilemma import Dilemma, C, D

class Sema4All_Killer(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        """Sema4All_Killer"""
        super().__init__(dilemma,name)
        self.first_movement = C

    def strategy(self, opponent: Player) -> int:
        """
        - First round it cooperates, then, the strategy is the stay-shift one.
        - It also includes a low random percentage (1%) from the second move to decide at random 
        if it cooperates or defects, giving more weight to defect (60%).
        - It is based on the strategy called: ADAPTIVE PAVLOV
        """
        if self.iteration < 2:
            self.iteration += 1 
            return self.first_movement
        
        if random.randint(0, 100) < 1:
            if random.random() > 0.4:
                return D
            else:
                return C
        
        if self.history[-1] == opponent.history[-1]:
            return self.history[-1]
        else:
            self.history[-1] = 1 - self.history[-1]
            return self.history[-1]
# -----------------------------------------------------------------  
