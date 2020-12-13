from typing import List

from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants


def _get_nearest_treasure(location, treasure_list):
    if treasure_list:
        treasure_distance = 10
        closest_treasure = treasure_list[0]
        for treasure in treasure_list:
            new_treasure_dist = utils.manhattan_distance(location, treasure)
            if new_treasure_dist < treasure_distance:
                treasure_distance = new_treasure_dist
                closest_treasure = treasure
        return closest_treasure
    else:
        return None
    
def get_reachable_treasure(location, treasure_list, game_state: object):
    list_treasures = []
    for treasure in treasure_list:
        path = utils.get_shortest_path(location, treasure, game_state)
        if path:
            list_treasures.append(treasure)
    return list_treasures


class TreasureStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        treasure = game_state.treasure
        treasures = get_reachable_treasure(location, treasure, game_state)
        # get the nearest treasure to the player
        nearest_treasure = _get_nearest_treasure(location, treasures)
        # navigate to the treasure
        if nearest_treasure is not None:
            path = utils.get_shortest_path(location, nearest_treasure, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            return action_seq

        return [constants.ACTIONS["none"]]
