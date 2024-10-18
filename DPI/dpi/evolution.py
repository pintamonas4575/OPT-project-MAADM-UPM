from __future__ import annotations

import numpy as np
import itertools
import copy
import math
import matplotlib.pyplot as plt
from player import Player, Tft, Cooperator, Defector
from dilemma import Dilemma
from game import Game

class Evolution:

    # Este método ya está implementado
    def __init__(self, players: tuple[Player, ...],
                       n_rounds: int = 100,
                       error: float = 0.0,
                       repetitions: int = 2,
                       generations: int = 100,
                       reproductivity: float = 0.05,
                       initial_population: tuple[int, ...] | int = 100):
        """
        Evolutionary tournament

        Parameters:
            - players (tuple[Player, ...]): tuple of players that will play the
         tournament
            - n_rounds (int = 100): number of rounds in each game
            - error (float = 0.0): error probability (in base 1)
            - repetitions (int = 2): number of games each player plays against
         the rest
            - generations (int = 100): number of generations to simulate
            - reproductivity (float = 0.05): ratio (base 1) of worst players
         that will be removed and substituted by the top ones in the natural
         selection process carried out at the end of each generation
            - initial_population (tuple[int, ...] | int = 100): list of
         individuals representing each players (same index as 'players' tuple)
         OR total population size (int).
        """

        self.players = players
        self.n_rounds = n_rounds
        self.error = error
        self.repetitions = repetitions
        self.generations = generations
        self.reproductivity = reproductivity

        if isinstance(initial_population, int):
            self.initial_population = [math.floor(initial_population
                                       / len(self.players))
                                       for _ in range(len(self.players))]
        else:
            self.initial_population = initial_population

        self.total_population = sum(self.initial_population)
        self.repr_int = int(self.total_population * self.reproductivity)

        self.ranking = {copy.deepcopy(player): 0.0 for i, player in
                        enumerate(self.players)
                       for _ in range(self.initial_population[i])}

    def natural_selection(self, result_tournament: dict[Player, float]) \
                          -> tuple[list,list]:
        """
        Kill the worst guys, reproduce the top ones. Takes the ranking once a
        face-to-face tournament has been played and returns another ranking,
        with the evolutionary changes applied

        Parameters:
            - result_tournament: the 'tournament.ranking' kind of dict.

        Results:
            - Same kind of dict ranking as the input, but with the evolutionary
         dynamics applied
        """
        
        n = int(len(result_tournament) * self.reproductivity)    # n is the number of individuals that will be reaplaced

        # El ranking ya esá ordenado
        population_without_n_worst_individuals = list(result_tournament.keys())[0:-n]
        n_best_individuals = list(result_tournament.keys())[0:n]

        new_generation_population = {player.name: [0] for player in self.players}

        # Añadimos todos los individuos menos los n peores
        for individual in population_without_n_worst_individuals:
            new_generation_population[individual.name][0] = new_generation_population[individual.name][0] + 1
        
        # En vez de añadir los n peores, volvemos a añadir los 5 mejores
        for individual in n_best_individuals:
            new_generation_population[individual.name][0] = new_generation_population[individual.name][0] + 1

        return new_generation_population


    def count_strategies(self) -> dict[str, int]:
        """
        Counts the number of played alive of each strategy, based on the
        initial list of players. Should be computed analyzing the
        'self.ranking' variable. Useful for the results plot/print (not needed
        for the tournament itself)

        Results:
            - A dict, containing as values the name of the players and as
         values the number of individuals they have now alive in the tournament
        """
        raise NotImplementedError

    def play(self, do_print: bool = False):
        """
        Main call of the class. Performs the computations to simulate the
        evolutionary tournament.

        Parameters
            - do_print (bool = False): if True, should print the ongoing
         results at the end of each generation (i.e. print generation number,
         and number of individuals playing each strategy).
        """

        # HINT: Initialise the following variable
        #  > count_evolution = {player.name: [val] for player, val in
        #                       zip(self.players, self.initial_population)}
        # and use it to store the number of individuals each player retains at
        # the end of each generation, appending to its corresponding list value
        # the number of individuals each player has (obtained by calling
        # 'self.count_strategies()'). For example, at some point, it could have
        # the following value:
        # {'cooperator': [15, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0],
        #  'defector': [5, 10, 15, 19, 14, 9, 4, 0, 0, 0, 0],
        #  'tft': [5, 5, 5, 6, 11, 16, 21, 25, 25, 25, 25]}

        count_evolution = {player.name: [val] for player, val in zip(self.players, self.initial_population)}
        
        for gen in range(self.generations):

            # Ejectuamos el DP no iterativo
            self.ranking = {copy.deepcopy(player): 0.0 for i, player in
                enumerate(self.players)
                for _ in range(count_evolution[player.name][gen])}

            combinations = list(itertools.combinations(list(self.ranking.keys()), 2))
            for repetetion in range(self.repetitions):
                for combination in combinations:
                    game=Game(combination[0],combination[1],self.n_rounds,self.error)
                    game.play(True)
                    combination[0].clean_history()
                    combination[1].clean_history()
                    score_0,score_1=game.score

                    self.ranking[combination[0]] = self.ranking[combination[0]] + score_0
                    self.ranking[combination[1]] = self.ranking[combination[1]] + score_1
            
            self.sort_ranking()
            
            # Se realiza la selección
            next_generation = self.natural_selection(self.ranking)

            for player in self.players:
                if(player.name in next_generation):
                    count_evolution[player.name].extend(next_generation[player.name])
                else:
                    count_evolution[player.name].extend([0])
                    
        self.stackplot(count_evolution)
    
    def sort_ranking(self) -> None:
        self.ranking = dict(sorted(self.ranking.items(), key=lambda item: item[1],reverse=True))

    # Si quieres obtener un buen gráfico de la evolución, puedes usar este
    # método si has seguido la pista indicada en la cabecera del método
    # anterior. Ya está implementado, pero puede que necesites adaptarlo a tu
    # código.
    def stackplot(self, count_evolution: dict[str, list]) -> None:
        """
        Plots a 'stackplot' of the evolution of the tournament

        Parameters:
            - count_evolution (dict[Player, list]): a dictionary containing as
         keys the name of the strategies of the different players of the
         tournament. Each value is a list, where the 'i'-th position of that
         list indicates the number of individuals that player has at the end of
         the 'i'-th generation
         """

        COLORS = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']

        for i, name in enumerate(count_evolution.keys()):
            plt.plot([], [], label=name, color= COLORS[(i) % len(COLORS)])

        plt.stackplot(list(range(self.generations + 1)),
                      np.array(list(count_evolution.values())), colors=COLORS)

        plt.legend()
        plt.show()
# ------------------------------------------------------
dilemma = Dilemma(2, -1, 3, 0)

cooperator_player = Cooperator(dilemma, "cooperator")
defector_player = Defector(dilemma, "defector")
tft_player = Tft(dilemma, "tft")

all_players = (cooperator_player, defector_player, tft_player)

evolution = Evolution(all_players, n_rounds=10, error=0.00, repetitions=1,
                      generations=10, reproductivity=0.2,
                      initial_population=(15, 5, 5))

evolution.play(True)