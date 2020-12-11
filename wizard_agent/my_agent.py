"""
TEMPLATE for creating your own Agent to compete in
'Dungeons and Data Structures' at the Coder One AI Sports Challenge 2020.
For more info and resources, check out: https://bit.ly/aisportschallenge

BIO:
This is our agent. He does things. Yay

"""
from . import brain

# import time
# import numpy as np
# import pandas as pd
# import sklearn


class Agent:
	def __init__(self):
		self.strategies = {
			'random': brain.RandomStrategy()
		}

	def next_move(self, game_state, player_state):
		"""
		This method is called each time your Agent is required to choose an action
		"""
		strategy = self.strategies['random']
		return strategy.execute(game_state, player_state)
