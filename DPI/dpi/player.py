from __future__ import annotations

import numpy as np
from abc import ABC, abstractmethod
from dilemma import Dilemma, C, D

class Player(ABC):

    @abstractmethod
    def __init__(self, dilemma: Dilemma, name: str = ""):
        """
        Abstract class that represents a generic player

        Parameters:
            - name (str): the name of the strategy
            - dilemma (Dilemma): the dilemma that this player will play
        """

        self.name = name
        self.dilemma = dilemma

        self.history  = []  # This is the main variable of this class. It is
                            # intended to store all the history of actions
                            # performed by this player.
                            # Example: [C, C, D, D, D] <- So far, the
                            # interaction lasts five rounds. In the first one,
                            # this player cooperated. In the second, he also
                            # cooperated. In the third, he defected. Etc.
        self.trust=True
        self.iteration=0

    @abstractmethod
    def strategy(self, opponent: Player) -> int:
        """
        Main call of the class. Gives the action for the following round of the
        interaction, based on the history

        Parameters:
            - opponent (Player): is another instance of Player.

        Results:
            - An integer representing Cooperation (C=0) or Defection (D=1)
        """
        pass

    def compute_scores(self, opponent: Player) -> tuple[float, float]:
        """
        Compute the scores for a given opponent

        Parameters:
            - opponent (Player): is another instance of Player.

        Results:
            - A tuple of two floats, where the first value is the current
            player's payoff, and the second value is the opponent's payoff.
        """
        other_player_actions=opponent.history
        results = np.array([self.dilemma.evaluate_result(action1,action2) for action1,action2 in zip(self.history,other_player_actions)])
        current_player_payoff=results[:,0].sum()
        opponent_player_payoff=results[:,1].sum()
        return int(current_player_payoff), int(opponent_player_payoff)

    def clean_history(self):
        """Resets the history of the current player"""
        self.history = []
        self.iteration=0
        self.trust=True
# ----------------------------------------------------------
# Las 5 estrategias básicas del juego de Nicky Case
class Cooperator(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        """Cooperator"""
        super().__init__(dilemma,name)

    def strategy(self, opponent: Player) -> int:
        """Cooperates always"""
        return C
# ------------------------------------------------------------
class Defector(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        """Defector"""
        super().__init__(dilemma,name)

    def strategy(self, opponent: Player) -> int:
        """Defects always"""
        return D
# ------------------------------------------------------------
class Tft(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        """Tit-for-tat"""
        super().__init__(dilemma,name)

    def strategy(self, opponent: Player) -> int:
        """Cooperates first, then repeat last action of the opponent"""

        if self.trust:
            if D in opponent.history:
                self.trust = False
                return opponent.history[-1]
            return C
        else:
            return opponent.history[-1]
# ------------------------------------------------------------
class Grudger(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        """Grudger"""
        super().__init__(dilemma,name)

    def strategy(self, opponent: Player) -> int:
        """
        Cooperates always, but if opponent ever defects, it will defect for the
        rest of the game
        """
        if self.trust:
            if D in opponent.history:
                self.trust = False
                return D
            return C
        else:
            return D
# ------------------------------------------------------------
class Detective4MovsTft(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        """Four movement - tit for tat detective"""
        super().__init__(dilemma,name)
        self.first_movements=[C,D,C,C]

    def strategy(self, opponent: Player) -> int:
        """
        Starts with a fixed sequence of actions: [C,D,C,C]. After that, if
        the opponent has ever defected, plays 'TFT'. If not, plays 'Defector'.
        """
        if self.iteration <= 3:
            self.iteration+=1
            return self.first_movements[self.iteration-1]
        else:
            if D in opponent.history:
                return opponent.history[-1]
            else:
                return D
# ------------------------------------------------------------
class Destructomatic(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        super().__init__(dilemma, name)
        self.defection_count = 0
        self.consecutive_cooperation = 0
        self.rounds_to_defect = 0

    def strategy(self, opponent: Player) -> int:
        """
        A gradual forgiveness strategy.
        Starts cooperating, increases defection periods for repeated defections,
        and resets after a series of cooperations.
        """

        turns = len(self.history)

        if turns == 0:  # First move, always cooperate
            return C

        if self.rounds_to_defect > 0:
            self.rounds_to_defect -= 1
            return D  # Defect if we're in a defection period

        last_move = opponent.history[-1]

        if last_move == C:
            self.consecutive_cooperation += 1
            if self.consecutive_cooperation >= 5:
                self.defection_count = 0
                self.consecutive_cooperation = 0
        else:  # Opponent defected
            self.defection_count += 1
            self.consecutive_cooperation = 0
            self.rounds_to_defect = self.defection_count
            return D  # Defect immediately after opponent's defection

        return C  # Cooperate otherwise
# ------------------------------------------------------------
class Periodic_CD(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        super().__init__(dilemma,name)
        self.movements=[C,D]

    def strategy(self, opponent: Player) -> int:
        self.iteration += 1
        return self.movements[(self.iteration-1) % 2]
# ------------------------------------------------------------
class Periodic_DC(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        super().__init__(dilemma,name)
        self.movements=[D,C]

    def strategy(self, opponent: Player) -> int:
        self.iteration += 1
        return self.movements[(self.iteration-1) % 2]
# ------------------------------------------------------------
class Periodic_CCD(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        super().__init__(dilemma,name)
        self.movements=[C,C,D]

    def strategy(self, opponent: Player) -> int:
        self.iteration += 1
        return self.movements[(self.iteration-1) % 3]
# ------------------------------------------------------------
class Periodic_CDD(Player):

    def __init__(self, dilemma: Dilemma, name: str = ""):
        super().__init__(dilemma,name)
        self.movements=[C,D,D]

    def strategy(self, opponent: Player) -> int:
        self.iteration += 1
        return self.movements[(self.iteration-1) % 3]
# ------------------------------------------------------------