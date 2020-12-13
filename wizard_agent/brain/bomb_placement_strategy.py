from typing import List
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants


class BombPlacementStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        wood_blocks = game_state.soft_blocks
        location = player_state.location

        # get the nearest block to the player
        reachable_wood_blocks = utils.get_reachable_tiles(location, wood_blocks, game_state)
        nearest_wood_block = utils.get_nearest_tile(location, reachable_wood_blocks)

        surrounding_tiles = utils.get_surrounding_tiles(nearest_wood_block, game_state)
        empty_tiles = utils.get_empty_tiles(surrounding_tiles, game_state)

        # navigate to the wood_block
        if nearest_wood_block is not None:
            tile_near_block = utils.get_nearest_tile(location, empty_tiles)
            if tile_near_block:
                path = utils.get_shortest_path(location, tile_near_block, game_state)
                action_seq = utils.get_path_action_seq(location, path)
                action_seq.append(constants.ACTIONS["bomb"])
                return action_seq
        return [constants.ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        ammo = player_state.ammo

        wood_blocks = game_state.soft_blocks
        location = player_state.location

        # get the nearest block to the player
        reachable_wood_blocks = utils.get_reachable_tiles(location, wood_blocks, game_state)
        nearest_wood_block = utils.get_nearest_tile(location, reachable_wood_blocks)

        surrounding_tiles = utils.get_surrounding_tiles(nearest_wood_block, game_state)
        empty_tiles = utils.get_empty_tiles(surrounding_tiles, game_state)

        return ammo > 0 and len(empty_tiles) > 0
