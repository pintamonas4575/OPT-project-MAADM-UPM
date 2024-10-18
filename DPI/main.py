from __future__ import annotations

from dpi.dilemma import Dilemma
from dpi.player import Player, Cooperator, Defector, Tft, Grudger, Detective4MovsTft, Destructomatic
from dpi.game import Game
from dpi.tournament import Tournament 
from dpi.sema4all_killer import Sema4All_Killer

dilemma = Dilemma(13, 0, 20, 4)
participants = (Destructomatic(dilemma, "destr"),
                Cooperator(dilemma, "coop1"),
                Defector(dilemma, "defect"),
                Cooperator(dilemma, "coop2"),
                Tft(dilemma, "tft"),
                Detective4MovsTft(dilemma, "detect"))

tournament = Tournament(participants, dilemma, n_rounds=100, error=0.01, repetitions=2)
tournament.play()
# tournament.plot_results()