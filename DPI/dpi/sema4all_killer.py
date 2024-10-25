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
        First round it cooperates, then, the strategy is the stay-shift one.
        It also includes a low random percentage (1%) from the second move to decide at random 
        if it cooperates or defects, giving more weight to defect (60%).
        It is based on the strategy called: ADAPTIVE PAVLOV
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
# class Sema4All_Killer(Player): # AdaptiveTFT
#     def __init__(self, dilemma: Dilemma, name: str = ""):
#         """Sema4All_Killer"""
#         super().__init__(dilemma,name)
#         self.cooperation = True  # Comienza cooperando (0)
#         self.recent_deserts = 0  # Conteo de deserciones recientes del oponente
#         self.max_deserts = 2     # Máximo de deserciones permitidas antes de castigar
#         self.forgive_prob = 0.2  # Probabilidad de perdonar una deserción ocasional

#     def strategy(self, opponent: Player) -> int:

#         if len(opponent.history) == 0:
#             return C
        
#         if opponent.history[-1] == 1:  # El oponente desertó
#             self.recent_deserts += 1
#         else:  # El oponente cooperó
#             self.recent_deserts = 0

#         if self.recent_deserts > self.max_deserts:
#             # Castiga si el oponente deserta repetidamente
#             self.cooperation = False
#         else:
#             # Ocasionalmente perdona una deserción para evitar ciclos negativos
#             if opponent.history[-1] == 1 and random.random() < self.forgive_prob:
#                 self.cooperation = True
#             else:
#                 # Sigue el comportamiento del oponente
#                 self.cooperation = (opponent.history[-1] == 0)

#         # Retornamos 0 si cooperamos, 1 si desertamos
#         return 0 if self.cooperation else 1
