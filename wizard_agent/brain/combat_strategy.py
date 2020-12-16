from typing import List

from .strategy import Strategy
from .utils import util_functions as utils


class CombatStrategy(Strategy):
    def __init__(self):
        self.game_state = None
        self.player_state = None
        self.escape_paths = []  # escape paths for each tile in map

    def execute(self, game_state: object, player_state: object) -> List[str]:
        self.game_state = game_state
        self.player_state = player_state
        # areas of interest
        # calculate advantage

    def can_execute(self, game_state: object, player_state: object) -> bool:
        self.game_state = game_state
        self.player_state = player_state
        self.escape_paths = utils.get_escape_matrix(game_state)
        return True

    def get_score(self):
        pass
