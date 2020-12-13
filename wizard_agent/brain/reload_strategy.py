from typing import List

from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants


def _get_nearest_ammo(location, ammo_list):
    if ammo_list:
        ammo_distance = 10
        closest_ammo = ammo_list[0]
        for ammo in ammo_list:
            new_ammo_dist = utils.manhattan_distance(location, ammo)
            if new_ammo_dist < ammo_distance:
                ammo_distance = new_ammo_dist
                closest_ammo = ammo
        return closest_ammo
    else:
        return None


class ReloadStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        ammo = game_state.ammo
        location = player_state.location
        ammos = utils.get_reachable_ammo(location, ammo, game_state)
        # get the nearest ammo to the player
        nearest_ammo = _get_nearest_ammo(location, ammos)
        # navigate to the ammo
        if nearest_ammo is not None:
            path = utils.get_shortest_path(location, nearest_ammo, game_state)
            action_seq = utils.get_path_action_seq(location, path)
            return action_seq

        return [constants.ACTIONS["none"]]
