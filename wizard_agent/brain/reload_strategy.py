from typing import List

from . import strategy


class ReloadStrategy(strategy.Strategy):
    def execute(self, game_state: object, player_state: object) -> List[str]:
        pass
