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
        """A veces le da un TIC en el que no se sabe qué es lo que sacará"""
        self.iteration += 1

        if self.iteration < 2: # la nº '0' y '1'
            return self.first_movements[self.iteration]
        
        if self.iteration % 3 == 0:  # caso periódico de TIC
            if random.random()+0.1 > 0.5:
                return D
        else:
            return C
        
        # analizar últimos 3 movimientos del oponente
        last_opponent_moves = opponent.history[:-3]
        return max(set(last_opponent_moves), key=last_opponent_moves.count)

