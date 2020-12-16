from typing import List

from .strategy import Strategy
from .utils import util_functions as utils


class CombatStrategy(Strategy):
    def __init__(self):
        self.game_state = None
        self.player_state = None
        self.escape_matrix = []  # num of escape paths for each tile in map
        self.has_advantage = False

    def execute(self, game_state: object, player_state: object) -> List[str]:
        self.game_state = game_state
        self.player_state = player_state
        # areas of interest
        location = player_state.location
        ammo = player_state.ammo
        if ammo > 0:  # can be aggressive
            opponent_list = game_state.opponents(player_state.id)
            opponent = utils.get_opponent(location, opponent_list)
            # check strategy conditions
            enemy_escape = self.get_escape_path(opponent)  # number of escape paths opponent has
            dist_from_enemy = utils.manhattan_distance(location, opponent)
            # if enemy is vulnerable, trap them
            if enemy_escape <= 2:
                return self.trap_enemy(location, opponent)
            # if enemy is 1 or 2 blocks from us, put bomb next to them so they GTFO
            elif dist_from_enemy <= 2:
                return self.place_bomb(location, opponent)
            # check if it can do some fake outs
            elif self.can_fake_out(location, opponent):
                return self.fake_out(location, opponent)
            # if it can chain bombs, go to tile that can make big boom
            elif self.can_chain_bomb(location):
                return self.chain_bombs(location)

        # defensive strategy
        return self.retreat_to_safe(location)

    def can_execute(self, game_state: object, player_state: object) -> bool:
        self.game_state = game_state
        self.player_state = player_state
        self.escape_matrix = utils.get_escape_matrix(game_state)
        location = player_state.location
        opponent_list = game_state.opponents(player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        # check if it can execute any aggressive
        enemy_escape = self.get_escape_path(opponent)  # number of escape paths opponent has
        dist_from_enemy = utils.manhattan_distance(location, opponent)
        can_chain_bomb = self.can_chain_bomb(location)
        can_fake_out = self.can_fake_out(location, opponent)
        self.has_advantage = enemy_escape <= 2 or dist_from_enemy <= 2 or can_chain_bomb

        return True

    # Offensive conditions

    def can_fake_out(self, location, opponent):
        return False

    def can_chain_bomb(self, location):
        return False

    # Offensive Strategies

    def fake_out(self, location, opponent):
        return []

    def place_bomb(self, location, enemy):
        return []

    def trap_enemy(self, location, opponent):
        return []

    def chain_bombs(self, location):
        return []

    # Defensive Strategies

    def retreat_to_safe(self, location):
        escape_paths = self.get_escape_path(location)
        return []

    # Helper functions

    def get_escape_path(self, tile):
        empty_tiles = utils.get_surrounding_empty_tiles(tile, self.game_state)
        return len(empty_tiles)

    def get_score(self):
        pass
