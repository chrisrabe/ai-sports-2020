from typing import List
import random
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants
ore_state = {}

# check if any of the values in ore_state is equal to 1
def ore_checker(ore_state):
    urgent_ore = []
    for key, value in ore_state.items():
        if value == 1:
            urgent_ore.append(tuple(key))
        
    return urgent_ore

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


class OreBombStrategy(strategy.Strategy):
    
    def execute(self, game_state: object, player_state: object) -> List[str]:
        
        ore_blocks = game_state.ore_blocks
        location = player_state.location

        if ore_state == {}:
            for ore in ore_blocks:
                ore_state[ore] = 3
        
        urgent_ore = ore_checker(ore_state)
        print(urgent_ore)
        # get the nearest block to the player
        if urgent_ore:
            nearest_ore_block_location = urgent_ore[0]
            ore_state[nearest_ore_block_location] = ore_state[nearest_ore_block_location] - 1
        else:
            nearest_ore_block_location = _get_nearest_ore_block(location, ore_blocks)
            ore_state[nearest_ore_block_location] = ore_state[nearest_ore_block_location] - 1

        surrounding_tiles = utils.get_surrounding_tiles(nearest_ore_block_location, game_state)
        empty_tiles = utils.get_empty_tiles(surrounding_tiles, game_state)

        # navigate to the ore_block
        if nearest_ore_block_location is not None:
            tile_near_block = utils.get_tile_next_to_block(location, empty_tiles, nearest_ore_block_location)
            if tile_near_block is not None:
                path = utils.get_shortest_path(location, tile_near_block, game_state)
                action_seq = utils.get_path_action_seq(location, path)
                action_seq.append(constants.ACTIONS["bomb"])
                return action_seq

        return [constants.ACTIONS["none"]]
