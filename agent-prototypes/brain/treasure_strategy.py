from typing import List
import random
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants


class FleeStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        location = player_state.location
        bombs = game_state.bombs

        surrounding_tiles = utils.get_surrounding_tiles(location, game_state)
        empty_tiles = utils.get_empty_tiles(surrounding_tiles, game_state)

        if empty_tiles:
            # get the safest tile for us to move to
            safest_tile = utils.get_safest_tile(location, empty_tiles, bombs)
            return [utils.move_to_tile(location, safest_tile)]
        else:
            return [random.choice(constants.ACTION_LIST)]
