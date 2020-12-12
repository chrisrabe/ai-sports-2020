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
		self.action_queue = []

	def next_move(self, game_state, player_state):
		"""
		This method is called each time your Agent is required to choose an action
		"""

		# if queue is empty, get strategy
		if not self.action_queue:
			strategy = self.strategies['random']
			actions = strategy.execute(game_state, player_state)
			self.action_queue = self.action_queue + actions

		# return the action on front of queue
		return self.action_queue.pop(0)
