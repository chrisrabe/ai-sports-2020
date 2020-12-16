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
            'orebomb': brain.OreBombStrategy(),
            'kill': brain.KillStrategy(),
            'retreat': brain.RetreatStrategy(),
            'smartbomb': brain.SmartBombStrategy(),
            'smartcollect' : brain.SmartCollectionStrategy(),
        }
        self.action_queue = []
        self.ore_state = {}

    def next_move(self, game_state, player_state):
        """This method is called each time your Agent is required to choose an action"""

        # if queue is empty, get strategy
        if not self.action_queue:
            strategy_name = "retreat"
            can_do_flee = self.strategies["flee"].can_execute(game_state, player_state)
            can_do_bomb = self.strategies["smartbomb"].can_execute(game_state, player_state)
            can_do_kill = self.strategies["kill"].can_execute(game_state, player_state)
            can_do_collect = self.strategies["smartcollect"].can_execute(game_state,player_state)
            # Determine next action
            if can_do_flee:
                strategy_name = 'flee'
            elif can_do_bomb:
                strategy_name = 'smartbomb'
            elif can_do_kill:
                strategy_name = 'kill'
            elif can_do_collect:
                strategy_name = 'smartcollect'


            # enqueue next action sequence
            strategy = self.strategies[strategy_name]
            actions = strategy.execute(game_state, player_state)
            self.action_queue = self.action_queue + actions

        # execute the first action
        return self.action_queue.pop(0)
