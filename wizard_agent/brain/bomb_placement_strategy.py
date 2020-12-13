from typing import List
import random
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants

def _get_nearest_wood_block(location, wood_block_list):
    if wood_block_list:
        wood_block_distance = 10
        closest_wood_block = wood_block_list[0]
        for wood_block in wood_block_list:
            new_wood_block_dist = utils.manhattan_distance(location, wood_block)
            if new_wood_block_dist < wood_block_distance:
                wood_block_distance = new_wood_block_dist
                closest_wood_block = wood_block
        return closest_wood_block
    else:
        return None

def get_tile_next_to_block(location, tiles, wood_blocks):
    """
    Given a list of tiles and wooden blocks, find the tile that's closest empty tile to move to
    """

    block_distance = 10
    closest_block = wood_blocks[0]

    for block in wood_blocks:
        new_block_distance = utils.manhattan_distance(block, location)
        if new_block_distance < block_distance:
            block_distance = new_block_distance
            closest_block = block

    empty_tile_near_block_dict = {}
    for tile in tiles:
        distance = utils.manhattan_distance(closest_block, tile)
        empty_tile_near_block_dict[tile] = distance

    # return the tile with the furthest distance from any bomb

    if len(empty_tile_near_block_dict) > 0: 
        best_tile = min(empty_tile_near_block_dict, key=empty_tile_near_block_dict.get)
        return best_tile
    else:
        return None
    

class BombPlacementStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:

        
        wood_blocks = game_state.soft_blocks
        location = player_state.location
        # get the nearest block to the player
        nearest_wood_block_location = _get_nearest_wood_block(location, wood_blocks)

        surrounding_tiles = utils.get_surrounding_tiles(nearest_wood_block_location, game_state)
        empty_tiles = utils.get_empty_tiles(surrounding_tiles, game_state)

        # navigate to the wood_block
        if nearest_wood_block_location is not None:
            tile_near_block = get_tile_next_to_block(location, empty_tiles, wood_blocks)
            path = utils.get_shortest_path(location, tile_near_block, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            action_seq.append(constants.ACTIONS["bomb"])
            return action_seq
        else:
            return [constants.ACTIONS["none"]]