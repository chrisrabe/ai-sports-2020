from typing import List
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants


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


def get_surrounding_empty_tiles(location, game_state):
    """
    Retrieves surrounding walkable tile around the location
    """
    surrounding_tiles = utils.get_surrounding_tiles(location, game_state)
    empty_tiles = utils.get_empty_tiles(surrounding_tiles, game_state)
    return empty_tiles


def get_safe_tiles(danger_tiles, game_state):
    """
    Retrieves all the safe walkable tiles outside of danger zone
    """
    safe_tiles = []
    for tile in danger_tiles:
        empty_tiles = get_surrounding_empty_tiles(tile, game_state)
        for empty in empty_tiles:
            if empty not in danger_tiles:
                safe_tiles.append(empty)
    return safe_tiles


class FleeStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        bombs = game_state.bombs

        bombs_in_range = utils.get_bombs_in_range(location, bombs)
        # get dangerous tiles
        dangerous_tiles = get_danger_zones(bombs_in_range, game_state)
        # find all safe areas
        safe_tiles = get_safe_tiles(dangerous_tiles, game_state)

