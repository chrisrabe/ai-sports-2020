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

def get_reachable_treasure(location, treasure_list, game_state: object):
    list_treasures = []
    for treasure in treasure_list:
        path = utils.get_shortest_path(location, treasure, game_state)
        if path:
            list_treasures.append(treasure)
    return list_treasures

def _get_nearest_ore_block(location, ore_block_list):
    if ore_block_list:
        ore_block_distance = 10
        closest_ore_block = ore_block_list[0]
        for ore_block in ore_block_list:
            new_ore_block_dist = utils.manhattan_distance(location, ore_block)
            if new_ore_block_dist < ore_block_distance:
                ore_block_distance = new_ore_block_dist
                closest_ore_block = ore_block
                
        return closest_ore_block
    else:
        return None


class Agent:
    def __init__(self):
        self.strategies = {
            'random': brain.RandomStrategy(),
            'flee': brain.FleeStrategy(),
            'move': brain.MoveStrategy(),
            'bomb': brain.BasicBombStrategy(),
            'reload': brain.ReloadStrategy(),
            'treasure': brain.TreasureStrategy(),
            'orebomb': brain.OreBombStrategy()
        }
        self.action_queue = []
        self.ore_state = {}

    def next_move(self, game_state, player_state):
        """This method is called each time your Agent is required to choose an action"""

        # if queue is empty, get strategy
        if not self.action_queue:
            strategy_name = "random"
            location = player_state.location
            bombs = game_state.bombs
            treasures = game_state.treasure
            ammo = player_state.ammo
            ores = game_state.ore_blocks
            nearest_ore_block_location = _get_nearest_ore_block(location, ores)
            surrounding_tiles = utils.get_surrounding_tiles(nearest_ore_block_location, game_state)
            empty_tiles = utils.get_empty_tiles(surrounding_tiles, game_state)
            tile_near_block = utils.get_tile_next_to_block(location, empty_tiles, nearest_ore_block_location)

            bombs_in_range = get_bombs_in_range(location, bombs)
            treasure_in_range = get_reachable_treasure(location, treasures, game_state)

            # Determine next action
            if game_state.entity_at(location) == 'b':
                strategy_name = 'move'
            elif ammo > 0 and tile_near_block:
                strategy_name = 'orebomb'
            elif treasure_in_range:
                strategy_name = 'treasure'
            elif bombs_in_range:
                strategy_name = 'flee'
            elif ammo == 0:
                strategy_name = 'reload'

            # enqueue next action sequence
            strategy = self.strategies[strategy_name]
            actions = strategy.execute(game_state, player_state)
            self.action_queue = self.action_queue + actions

        # execute the first action
        return self.action_queue.pop(0)
