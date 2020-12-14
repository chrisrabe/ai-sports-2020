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


def _get_furthest_ammo_from_opponent(opponent_location, ammo_list):
    if ammo_list and len(ammo_list) > 1:
        ammo_distance = 0
        furthest_ammo = ammo_list[0]
        for ammo in ammo_list:
            new_ammo_dist = utils.manhattan_distance(opponent_location, ammo)
            if new_ammo_dist > ammo_distance:
                ammo_distance = new_ammo_dist
                furthest_ammo = ammo
        return furthest_ammo
    else:
        return None


class ReloadStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        ammo = game_state.ammo
        location = player_state.location
        list_of_opponents = game_state.opponents(player_state.id)
        opponent_location = 0
        for opponent in list_of_opponents:
            opponent_location = opponent

        ammos = utils.get_reachable_tiles(location, ammo, game_state)
        # get the nearest ammo to the player
        nearest_ammo = _get_nearest_ammo(location, ammos)

        # get the furthest ammo from the opponent player
        furthest_ammo_from_opponent = _get_furthest_ammo_from_opponent(opponent_location, ammos)

        # navigate to the ammo
        if nearest_ammo is not None:
            if not utils.isOpponentCloser(location, opponent_location, nearest_ammo):
                path = utils.get_shortest_path(location, nearest_ammo, game_state)
                action_seq = utils.get_path_action_seq(location, path)
                return action_seq
            elif furthest_ammo_from_opponent is not None:
                path = utils.get_shortest_path(location, furthest_ammo_from_opponent, game_state)
                action_seq = utils.get_path_action_seq(location, path)
                return action_seq
        return [constants.ACTIONS["none"]]

    def can_execute(self, game_state: object, player_state: object) -> bool:
        player_ammo = player_state.ammo
        location = player_state.location
        list_of_opponents = game_state.opponents(player_state.id)
        opponent_location = 0
        for opponent in list_of_opponents:
            opponent_location = opponent
        ammo_pickups = game_state.ammo
        ammo_in_range = utils.get_reachable_tiles(location, ammo_pickups, game_state)
        furthest_ammo = _get_furthest_ammo_from_opponent(opponent_location, ammo_in_range)
        nearest_ammo = _get_nearest_ammo(location, ammo_in_range)
        
        return player_ammo < 3 and len(ammo_in_range) > 0 and nearest_ammo is not None or furthest_ammo is not None
