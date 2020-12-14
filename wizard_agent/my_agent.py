"""
TEMPLATE for creating your own Agent to compete in
'Dungeons and Data Structures' at the Coder One AI Sports Challenge 2020.
For more info and resources, check out: https://bit.ly/aisportschallenge

BIO:
This is our agent. He does things. Yay

"""

# import time
# import numpy as np
# import pandas as pd
# import sklearn
from . import brain

utils = brain.utils.util_functions


class Agent:
    def __init__(self):
        self.strategies = {
            'random': brain.RandomStrategy(),
            'flee': brain.FleeStrategy(),
            'move': brain.MoveStrategy(),
            'bomb': brain.BombPlacementStrategy(),
            'reload': brain.ReloadStrategy(),
            'treasure': brain.TreasureStrategy(),
            'orebomb': brain.OreBombStrategy(),
            'kill': brain.KillStrategy(),
            'retreat': brain.RetreatStrategy()
        }
        self.action_queue = []
        self.ore_state = {}

    def next_move(self, game_state, player_state):
        """This method is called each time your Agent is required to choose an action"""

        # if queue is empty, get strategy
        if not self.action_queue:
            strategy_name = "retreat"
            can_do_flee = self.strategies["flee"].can_execute(game_state, player_state)
            can_do_bomb = self.strategies["bomb"].can_execute(game_state, player_state)
            can_do_reload = self.strategies["reload"].can_execute(game_state, player_state)
            can_do_treasure = self.strategies["treasure"].can_execute(game_state, player_state)
            can_do_ore_bomb = self.strategies["orebomb"].can_execute(game_state, player_state)
            can_do_kill = self.strategies["kill"].can_execute(game_state, player_state)

            # Determine next action
            if can_do_treasure:
                strategy_name = 'treasure'
            elif can_do_flee:
                strategy_name = 'flee'
            elif can_do_bomb:
                strategy_name = 'bomb'
            elif can_do_ore_bomb:
                strategy_name = 'orebomb'
            elif can_do_reload:
                strategy_name = 'reload'
            if can_do_kill:
                strategy_name = 'kill'

            # enqueue next action sequence
            strategy = self.strategies[strategy_name]
            actions = strategy.execute(game_state, player_state)
            self.action_queue = self.action_queue + actions

        # execute the first action
        return self.action_queue.pop(0)
