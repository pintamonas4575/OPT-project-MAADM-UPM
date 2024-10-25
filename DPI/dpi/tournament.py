from __future__ import annotations

import itertools
import matplotlib.pyplot as plt
from game import Game
from player import Player
from dilemma import Dilemma
from player import Player, Cooperator, Defector, Tft, Grudger, Detective4MovsTft, Destructomatic
from player import Periodic_CD, Periodic_DC, Periodic_CCD, Periodic_CDD
from sema4all_killer import Sema4All_Killer

class Tournament:

    def __init__(self, players: tuple[Player, ...],
                       n_rounds: int = 100,
                       error: float = 0.0,
                       repetitions: int = 2):
        """
        All-against-all tournament

        Parameters:
            - players (tuple[Player, ...]): tuple of players that will play the
         tournament
            - n_rounds (int = 100): number of rounds in the game
            - error (float = 0.0): error probability (in base 1)
            - repetitions (int = 2): number of games each player plays against
         the rest
        """

        self.players = players
        self.n_rounds = n_rounds
        self.error = error
        self.repetitions = repetitions

        # This is a key variable of the class. It is intended to store the
        # ongoing ranking of the tournament. It is a dictionary whose keys are
        # the players in the tournament, and its corresponding values are the
        # points obtained in their interactions with each other. In the end, to
        # see the winner, it will be enough to sort this dictionary by the
        # values.
        self.ranking = {player: 0.0 for player in self.players}  # initial vals

    def sort_ranking(self) -> None:
        self.ranking = dict(sorted(self.ranking.items(), key=lambda item: item[1],reverse=True))

    #pista: utiliza 'itertools.combinations' para hacer los cruces
    def play(self) -> None:
        """
        Main call of the class. It must simulate the championship and update
        the variable 'self.ranking' with the accumulated points obtained by
        each player in their interactions.
        """
        combinations = list(itertools.combinations(self.players, 2))
        for repetetion in range(self.repetitions):
            for combination in combinations:
                game=Game(combination[0],combination[1],self.n_rounds,self.error)
                # print('*'*50)
                # print(f'Nuevo enfrentamiento{combination[0].name,combination[1].name}')
                game.play(do_print=False)
                combination[0].clean_history()
                combination[1].clean_history()
                score_0,score_1=game.score
                
                self.ranking[combination[0]] = self.ranking[combination[0]]+ score_0
                self.ranking[combination[1]] = self.ranking[combination[1]] +score_1
            self.sort_ranking()

    def plot_results(self):
        """
        Plots a bar chart of the final ranking. On the x-axis should appear
        the names of the sorted ranking of players participating in the
        tournament. On the y-axis the points obtained.
        """
        player_names = [x.name for x in self.ranking.keys()]
        player_scores = list(self.ranking.values())

        plt.figure(figsize=(14,5))
        plt.title(f"{self.n_rounds} rondas, {self.error} error, {self.repetitions} repeticiones")
        plt.bar(player_names, player_scores, color="Red")

        for i in range(len(player_names)):
            plt.text(x=i, y=player_scores[i], s=player_scores[i], ha = 'center', bbox = dict(facecolor = 'yellow', alpha =.8))
        
        plt.show()
# -----------------------------------------------
dilemma = Dilemma(2, -1, 3, 0)

# cooperator_player = Cooperator(dilemma, "cooperator")
# defector_player = Defector(dilemma, "defector")
tft_player = Tft(dilemma, "tft")
grudger_player = Grudger(dilemma, "grudger")
detective_player = Detective4MovsTft(dilemma, "detective")
periodic_cd  = Periodic_CD(dilemma, "periodic_cd")
periodic_dc  = Periodic_DC(dilemma, "periodic_dc")
periodic_ccd = Periodic_CCD(dilemma, "periodic_ccd")
periodic_cdd = Periodic_CDD(dilemma, "periodic_cdd")

destructor_player = Destructomatic(dilemma, "destructor")
sema4all_player = Sema4All_Killer(dilemma, "sema4all")

all_players = (tft_player, grudger_player, detective_player, destructor_player, sema4all_player,
               periodic_cd, periodic_dc, periodic_ccd, periodic_cdd,)

torneo = Tournament(all_players, n_rounds=150, error=0, repetitions=1)
torneo.play()
torneo.plot_results()
