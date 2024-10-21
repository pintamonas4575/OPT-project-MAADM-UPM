from __future__ import annotations

import random
from player import Player
from dilemma import Dilemma, C, D

class Sema4All_Killer(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        """Sema4All_Killer"""
        super().__init__(dilemma,name)

        self.first_movements=[C,C]
        self.opponent_defections = 0

    def strategy(self, opponent: Player) -> int:
        """"""
        if self.iteration < 2: # en las primeras se coopera
            self.iteration += 1
            return self.first_movements[self.iteration-1]
        
        if self.history[-1] == opponent.history[-1]:
            return self.history[-1]
        else:
            self.history[-1] = 1 - self.history[-1]
            return self.history[-1]
# -----------------------------------------------------------------  