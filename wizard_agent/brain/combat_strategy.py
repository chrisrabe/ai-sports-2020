from typing import List

from .strategy import Strategy
from .utils import util_functions as utils, constants


class CombatStrategy(Strategy):
    def __init__(self):
        self.game_state = None
        self.player_state = None
        self.escape_matrix = []  # num of escape paths for each tile in map
        self.has_advantage = False
        self.bomb_states = {}

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
        # variables of interest
        location = player_state.location
        opponent_list = game_state.opponents(player_state.id)
        opponent = utils.get_opponent(location, opponent_list)
        # initialise or update state variables
        self.escape_matrix = utils.get_escape_matrix(game_state)
        self.update_bomb_states()
        # check if it can execute any aggressive
        enemy_escape = self.get_escape_path(opponent)  # number of escape paths opponent has
        can_chain_bomb = self.can_chain_bomb(location)
        can_fake_out = self.can_fake_out(location, opponent)
        self.has_advantage = enemy_escape <= 2 or can_chain_bomb or can_fake_out

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

    def update_bomb_states(self):
        bombs = self.game_state.bombs
        cur_tick = self.game_state.tick_number
        # record new bombs
        for bomb in bombs:
            if bomb not in self.bomb_states:
                self.bomb_states[bomb] = cur_tick + constants.BOMB_DURATION
        # remove bombs that has passed its tick
        exploded_bombs = []
        for bomb, tick_due in self.bomb_states.items():
            if cur_tick >= tick_due:
                exploded_bombs.append(bomb)
        # delete them from bomb states
        for bomb in exploded_bombs:
            del self.bomb_states[bomb]

    def get_escape_path(self, tile):
        empty_tiles = utils.get_surrounding_empty_tiles(tile, self.game_state)
        return len(empty_tiles)
