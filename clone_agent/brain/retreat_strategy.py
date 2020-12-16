from typing import List
import random
from .strategy import Strategy
from .utils import util_functions as utils, constants


def get_opponent_danger_zone(opponent, game_state):
    max_dist = 3
    tile_queue = [opponent]
    danger_zones = []
    while len(tile_queue) > 0:
        cur_tile = tile_queue.pop(0)
        danger_zones.append(cur_tile)
        surrounding_tile = utils.get_surrounding_tiles(cur_tile, game_state)
        for tile in surrounding_tile:
            if utils.manhattan_distance(opponent, tile) <= max_dist and tile not in danger_zones:
                tile_queue.append(tile)
    return danger_zones


class RetreatStrategy(Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        opponent_list = game_state.opponents(player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        danger_zones = get_opponent_danger_zone(opponent, game_state)
        safe_zones = utils.get_safe_tiles(danger_zones, game_state)
        reachable_tiles = utils.get_reachable_tiles(location, safe_zones, game_state)
        nearest_tile = utils.get_nearest_tile(location, reachable_tiles)
        if nearest_tile is not None:
            path = utils.get_shortest_path(location, nearest_tile, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            return action_seq
        return [constants.ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        location = player_state.location
        opponent_list = game_state.opponents(player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        danger_zones = get_opponent_danger_zone(opponent, game_state)
        return location in danger_zones
