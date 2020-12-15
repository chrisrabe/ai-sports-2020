from typing import List
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants

ACTIONS = constants.ACTIONS

def get_danger_zones(bombs, game_state):
    """
    Retrieves the dangerous tiles
    """
    danger_tiles = []
    for bomb in bombs:
        blast_tiles = utils.get_blast_zone(bomb, game_state)
        for tile in blast_tiles:
            if tile not in danger_tiles:
                danger_tiles.append(tile)
    return danger_tiles


class StandStill(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        bombs = game_state.bombs

        
        bombs_in_range = utils.get_bombs_in_range(location, bombs)
        # get dangerous tiles
        dangerous_tiles = get_danger_zones(bombs_in_range, game_state)

        # wait if not standing in danger zone
        if location not in dangerous_tiles:
            return [ACTIONS["none"]]
        else:
            # find all safe areas
            safe_tiles = utils.get_safe_tiles(dangerous_tiles, game_state)
            reachable_tiles = utils.get_reachable_tiles(location, safe_tiles, game_state)

            # get nearest safe tile
            nearest_tile = utils.get_nearest_tile(location, reachable_tiles)

            #go to safe tile and stay there
            if nearest_tile:
                path = utils.get_shortest_path(location, nearest_tile, game_state)
                action_seq = utils.get_path_action_seq(location, path)
                 action_seq.append(ACTIONS["none"])
                return action_seq
            return [ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        location = player_state.location
        bombs = game_state.bombs
        bombs_in_range = utils.get_bombs_in_range(location, bombs)
        dangerous_tiles = get_danger_zones(bombs_in_range, game_state)
        return len(bombs_in_range) > 0 and location in dangerous_tiles
