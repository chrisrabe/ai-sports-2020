from typing import List
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants


def get_nearest_empty_wood_tile(game_state, player_state):
    wood_blocks = game_state.soft_blocks
    location = player_state.location

    # get the nearest block to wood near player
    empty_tiles_near_wood = utils.get_empty_locations(wood_blocks, game_state)
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
