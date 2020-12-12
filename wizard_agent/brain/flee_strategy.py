from typing import List

from . import strategy
from . import utils as _utils

utils = _utils.util_functions


class FleeStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        pass

