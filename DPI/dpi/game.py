from __future__ import annotations

import random
from dilemma import Dilemma, C, D
from player import Player, Cooperator, Defector, Tft, Grudger, Detective4MovsTft
from sema4all_killer import Sema4All_Killer

class Game:

    def __init__(self, player_1: Player,
                       player_2: Player,
                       n_rounds: int = 100,
                       error: float = 0.0):
        """
        Game class to represent an iterative dilema

        Parameters:
            - player_1 (Player): first player of the game
            - player_2 (Player): second player of the game
            - n_rounds (int = 100): number of rounds in the game
            - error (float = 0.0): error probability (in base 1)
        """

        assert n_rounds > 0, "'n_rounds' should be greater than 0"

        self.player_1 = player_1
        self.player_2 = player_2
        self.n_rounds = n_rounds
        self.error = error

        self.score = (0.0, 0.0)  # this variable will store the final result of
                                 # the game, once the 'play()' function has
                                 # been called. The two values of the tuple
                                 # correspond to the points scored by the first
                                 # and second player, respectively.


    def play(self, do_print: bool = False) -> None:
        """
        Main call of the class. Play the game.
        Stores the final result in 'self.score'

        Parameters
            - do_print (bool = False): if True, should print the ongoing
            results at the end of each round (i.e. print round number, last
            actions of both players and ongoing score).
        """
        for iteration in range(self.n_rounds):
            action_1=self.player_1.strategy(self.player_2)
            action_2=self.player_2.strategy(self.player_1)
            action_1,bool_1 = self.change_action(action_1)
            action_2,bool_2= self.change_action(action_2)
            self.player_1.history.append(action_1)
            self.player_2.history.append(action_2)

            if do_print:
                print('-'*50)
                print(f'Play number {iteration+1}:')
                if bool_1:
                    print(f'{self.player_1.name} played:{action_1}. Action was changed due to error probability.')
                else:
                    print(f'{self.player_1.name} played:{action_1}. Action was not changed.')
                if bool_2:
                    print(f'{self.player_2.name} played:{action_2}. Action was changed due to error probability.')
                else:
                    print(f'{self.player_2.name} played:{action_2}. Action was not changed.')
                print(self.player_1.compute_scores(self.player_2))
            
            self.score = (self.player_1.compute_scores(self.player_2))

    def plot_results(self, do_print: bool = False) -> None:
        if do_print:            
            print("*"*20)
            print(f"Players: {self.player_1.name} & {self.player_2.name}")
            print(f"Scores: {self.score}")
            print("*"*20)        

    def change_action(self, action):
        if random.random() < self.error:
            if action==C:
                return D, True
            else:
                return C, True
        else:
            return action, False
# -----------------------------------------------------------------
dilemma = Dilemma(2, -1, 3, 0)

cooperator_player = Cooperator(dilemma, "cooperator")
defector_player = Defector(dilemma, "defector")
tft_player = Tft(dilemma, "tft")
grudger_player = Grudger(dilemma, "grudger")
detective_player = Detective4MovsTft(dilemma, "detective")
sema4all_player = Sema4All_Killer(dilemma, "sema4all")

# Modifica las siguientes líneas a conveniencia para llevar a cabo distintos tests
# game = Game(sema4all_player, tft_player, n_rounds=50, error=0)
# game.play(do_print=False)
# game.plot_results(do_print=True)