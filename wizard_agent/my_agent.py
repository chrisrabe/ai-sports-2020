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


def get_bombs_in_range(location, bombs):
    bombs_in_range = []
    for bomb in bombs:
        distance = utils.manhattan_distance(location, bomb)
        if distance <= 10:
            bombs_in_range.append(bomb)
    return bombs_in_range

def get_treasure_in_range(location, treasure, game_state):
    treasures = get_reachable_treasure(location, treasure, game_state)
    if treasure:
        treasure_in_range = []
        for treasure in treasures:
            distance = utils.manhattan_distance(location, treasure)
            if distance <= 10:
                treasure_in_range.append(treasure)
        return treasure_in_range
    else:
        return []

def get_reachable_treasure(location, treasure_list, game_state: object):
    list_treasures = []
    for treasure in treasure_list:
        path = utils.get_shortest_path(location, treasure, game_state)
        if path:
            list_treasures.append(treasure)
    return list_treasures


class Agent:
    def __init__(self):
        self.strategies = {
            'random': brain.RandomStrategy(),
            'flee': brain.FleeStrategy(),
            'move': brain.MoveStrategy(),
            'bomb': brain.BasicBombStrategy(),
            'reload': brain.ReloadStrategy(),
            'treasure': brain.TreasureStrategy()
        }
        self.action_queue = []

    def next_move(self, game_state, player_state):
        """This method is called each time your Agent is required to choose an action"""

        # if queue is empty, get strategy
        if not self.action_queue:
            strategy_name = "random"
            location = player_state.location
            bombs = game_state.bombs
            treasures = game_state.treasure
            ammo = player_state.ammo

            bombs_in_range = get_bombs_in_range(location, bombs)
            treasure_in_range = get_treasure_in_range(location, treasures, game_state)

            # Determine next action
            if game_state.entity_at(location) == 'b':
                strategy_name = 'move'
            elif treasure_in_range:
                strategy_name = 'treasure'
            elif bombs_in_range:
                strategy_name = 'flee'
            elif ammo > 0:
                strategy_name = 'bomb'
            elif ammo == 0:
                strategy_name = 'reload'
            

            # enqueue next action sequence
            strategy = self.strategies[strategy_name]
            actions = strategy.execute(game_state, player_state)
            self.action_queue = self.action_queue + actions

        # execute the first action
        return self.action_queue.pop(0)