# from . import config
import numpy as np
import random
import os
from time import sleep

class agent:

	def __init__(self):
		self.actions = ['', 'l', 'r', 'u', 'd', 'p']

		# Initialise Q-table
		self.state_size = 12000
		self.action_size = len(self.actions)

		self.qtable = np.zeros((self.state_size, self.action_size))

		# Hyperparameters 
		self.learning_rate = 0.9
		self.discount_rate = 0.8
		self.epsilon = 1.0
		self.decay_rate = 0.01 

		# Variables controlling how long our agent will train for
		self.num_episodes = 50 
		# self.num_steps = 1800 # 1800 ticks 

		self.episode = 0
		# self.step = 0

	def get_surrounding_tiles(self, location):

		# find all the surrounding tiles relative to us
		# location[0] = col index; location[1] = row index
		tile_up = (location[0], location[1]+1)	
		tile_down = (location[0], location[1]-1)     
		tile_left = (location[0]-1, location[1]) 
		tile_right = (location[0]+1, location[1]) 		 

		# combine these into a list
		all_surrounding_tiles = [tile_up, tile_down, tile_left, tile_right]

		# we'll need to remove tiles that cross the border of the map
		# start with an empty list to store our valid surrounding tiles
		valid_surrounding_tiles = []

		# loop through our tiles
		for tile in all_surrounding_tiles:
			# check if the tile is within the boundaries of the game
			if self.game_state.is_in_bounds(tile):
				# if yes, then add them to our list
				valid_surrounding_tiles.append(tile)

		return valid_surrounding_tiles


	def predict_score(self, game_state, player_state, action):
		
		score_list = {
			'0' : -5, # Player 1
			'1' : -5, # Player 2
			'ib' : -10, # Metal Block
			'sb' : 10, # Wooden Block
			'ob' : 5, # Ore Block
			'b'  : -75,
			'a'  : 30,
			't'  : 80,
			None : 0,
		}

		def check_entity(tile):
			entity = game_state.entity_at(tile)
			reward = score_list[entity]
			return reward

		location = player_state.location

		tile_up = (location[0], location[1]+1)	
		tile_down = (location[0], location[1]-1)     
		tile_left = (location[0]-1, location[1]) 
		tile_right = (location[0]+1, location[1]) 


		direction = action

		if direction == 'u':
			reward = check_entity(tile_up)
			new_state = tile_up
		elif direction == 'd':
			reward = check_entity(tile_down)
			new_state = tile_down
		elif direction == 'l':
			reward = check_entity(tile_left)
			new_state = tile_left
		elif direction == 'r':
			reward = check_entity(tile_right)
			new_state = tile_right
		else:
			reward = 0
			new_state = (location[0], location[1])
		
		return new_state, reward

	def next_move(self, game_state, player_state):

		state = player_state.location
		self.episode +=1

		if random.uniform(0,1) < self.epsilon:
			 # Explore
			if player_state.ammo > 0:
				action = random.choice(self.actions) 
			else:
				action = random.choice(self.actions[:5])
		else:
			# Exploit
			if player_state.ammo > 0:


				action = self.actions[np.argmax(self.qtable[state,:])]
			
			else:
				action = self.actions[np.argmax(self.qtable[state,:5])]

		# Try an action and predict the reward
		new_state, reward = self.predict_score(game_state, player_state, action)

		action = self.actions.index(action)

		# Q-learning algorithm
		self.qtable[state,int(action)] = self.qtable[state,int(action)] + self.learning_rate * (reward + self.discount_rate * np.max(self.qtable[new_state,:]) - self.qtable[state,int(action)])

		# Decrease epsilon
		self.epsilon = np.exp(-self.decay_rate * self.episode)

		print(self.qtable)
 	
		return self.actions[action]
