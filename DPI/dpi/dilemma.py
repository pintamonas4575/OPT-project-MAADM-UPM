from __future__ import annotations

from abc import abstractmethod
import numpy as np
import itertools

class Dilemma:

    def __init__(self, cc: float, cd: float, dc: float, dd: float):
        """
        Represents a 2x2 symmetric dilemma.

        Parameters:
            - cc (float): payoff for mutual cooperation
            - cd (float): payoff when one cooperates, but the opponent defects
            - dc (float): payoff when one defects, and the opponent cooperates
            - dd (float): payoff for mutual defection
        """
        self.cc=cc
        self.cd=cd
        self.dc=dc
        self.dd=dd
        self.matrix=np.array([[self.cc,self.cd],[self.dc,self.dd]])


    @property
    @abstractmethod
    def payoff_matrix(self) -> np.ndarray:
        """
        Returns:
            - 2x2 np array of the matrix
        """
        return self.matrix


    @abstractmethod
    def evaluate_result(self, a_1: int, a_2: int) -> tuple[float, float]:
        """
        Given two actions, returns the payoffs of the two players.

        Parameters:
            - a_1 (int): action of player 1 ('C' or 'D', i.e. '1' or '0')
            - a_2 (int): action of player 2 ('C' or 'D', i.e. '1' or '0')

        Returns:
            - tuple of two floats, being the first and second values the payoff
            for the first and second player, respectively.
        """
        return int(self.matrix[a_1,a_2]),int(self.matrix[a_2,a_1])
# ---------------------------------------------------------- 
C = 0
D = 1

# All possible outcomes of the PD
pd = Dilemma(2, -1, 3, 0)
posible_actions = (C, D)
for a1, a2 in itertools.product(posible_actions, repeat=2):
    print(f"{(a1, a2)} -> {pd.evaluate_result(a1, a2)}")