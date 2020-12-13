from typing import List
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants


def get_surrounding_empty_tiles(location, game_state):
    """
    Retrieves surrounding walkable tile around the location
    """
    surrounding_tiles = utils.get_surrounding_tiles(location, game_state)
    empty_tiles = utils.get_empty_tiles(surrounding_tiles, game_state)
    return empty_tiles


def get_empty_locations(tiles, game_state):
    empty_locations = []
    for tile in tiles:
        empty_tiles = get_surrounding_empty_tiles(tile, game_state)
        empty_locations = empty_locations + empty_tiles
    return empty_locations


def get_nearest_empty_wood_tile(game_state, player_state):
    wood_blocks = game_state.soft_blocks
    location = player_state.location

    # get the nearest block to wood near player
    empty_tiles_near_wood = get_empty_locations(wood_blocks, game_state)
    reachable_tiles = utils.get_reachable_tiles(location, empty_tiles_near_wood, game_state)
    nearest_empty_tile = utils.get_nearest_tile(location, reachable_tiles)
    return nearest_empty_tile


class BombPlacementStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        nearest_empty_tile = get_nearest_empty_wood_tile(game_state, player_state)

        # navigate to the wood_block
        if nearest_empty_tile:
            path = utils.get_shortest_path(location, nearest_empty_tile, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            action_seq.append(constants.ACTIONS["bomb"])
            return action_seq
        return [constants.ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        ammo = player_state.ammo
        nearest_empty_tile = get_nearest_empty_wood_tile(game_state, player_state)
        return ammo > 0 and nearest_empty_tile
