from __future__ import annotations

from player import Player
from dilemma import Dilemma, C, D

class Sema4All_Killer(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        """Sema4All_Killer"""
        super().__init__(dilemma,name)

        raise NotImplementedError

    def strategy(self, opponent: Player) -> int:
        """"""
        raise NotImplementedError