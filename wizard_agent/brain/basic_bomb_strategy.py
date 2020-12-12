from typing import List
import random
from . import strategy
from . import utils as _utils

utils = _utils.util_functions
constants = _utils.constants


class BasicBombStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        return [constants.ACTIONS["bomb"]]
