"""
Interface for defining strategy pattern.
"""


class Strategy:
    def execute(self, game_state: object, player_state: object):
        """
        Execute the strategy
        """
        pass

