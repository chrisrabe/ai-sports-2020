"""
TEMPLATE for creating your own Agent to compete in
'Dungeons and Data Structures' at the Coder One AI Sports Challenge 2020.
For more info and resources, check out: https://bit.ly/aisportschallenge

BIO:
Agent using Q Learning 

"""

# import time
import numpy as np
import random
from time import sleep

from . import brain

# import pandas as pd
# import sklearn

# utils = brain.utils.util_functions

class Agent:

    def __init__(self, game_state):

        actions = ['','u','d','l','r','p']

        random.seed(42)

        N_STATES = game_state.size[0] * game_state.size[1]
        N_EPISODES = 20

        MAX_EPISODE_STEPS = 100

        MIN_ALPHA = 0.02

        alphas = np.linspace(1.0, MIN_ALPHA, N_EPISODES)
        gamma = 1.0
        eps = 0.2

        q_table = dict()

    def move_to_tile(self, location, tile):

        actions = ['', 'u', 'd', 'l','r','p']

        print(f"my tile: {tile}")

        # see where the tile is relative to our current location
        diff = tuple(x-y for x, y in zip(self.location, tile))

        # return the action that moves in the direction of the tile
        if diff == (0,1):
            action = 'd'
        elif diff == (1,0):
            action = 'l'
        elif diff == (0,-1):
            action = 'u'
        elif diff == (-1,0):
            action = 'r'
        else:
            action = ''

        return action

    def get_surrounding_tiles(self, location):

            # find all the surrounding tiles relative to us
            # location[0] = x-index; location[1] = y-index
            tile_up = (location[0], location[1]+1)  
            tile_down = (location[0], location[1]-1)
            tile_left = (location[0]-1, location[1])
            tile_right = (location[0]+1, location[1])        

            # combine these into a list
            all_surrounding_tiles = [tile_up, tile_down, tile_left, tile_right]

            # we'll need to include only the tiles that are within the game map boundaries
            # start with an empty list to store our valid surrounding tiles
            valid_surrounding_tiles = []

            # loop through our tiles
            for tile in all_surrounding_tiles:
                # check if the tile is within the boundaries of the game
                # NOTE: we add 'self' here because the object game_state 
                # is owned by the Agent class
                if self.game_state.is_in_bounds(tile): 
                    # if yes, then add them to our list
                    valid_surrounding_tiles.append(tile)
 
            return valid_surrounding_tiles



    def calculate_reward(self, game_state, location):

        reward_table = dict()

        for tile in location:

            if game_state.entity_at(tile) == 'b':
                reward_score = -100
            elif game_state.entity_at(tile) == 'a':
                reward_score = 60
            elif game_state.entity_at(tile) == 't':
                reward_score = 90
            elif game_state.entity_at(tile) == 'ob':
                reward_score = 20
            elif game_state.entity_at(tile) == 'ib':
                reward_score = 0
            elif game_state.entity_at(tile) == 'sb':
                reward_score = 5

            reward_table[tile] = reward_score

        return reward_table


    def act(self, location, action):
        '''
        Functions: 
            - Determine which tile is valid
            - Calculate the reward for each valid tile
            - Determine next action
        '''

        valid_surrounding_tiles = self.get_surrounding_tiles(location)

        # For each valid tiles, calculate reward / penalty
        reward_table = calculate_reward(valid_surrounding_tiles)
        reward = max(reward_table.values())  # maximum value
        target_tile = [k for k, v in dic.items() if v == max_value]

        return target_tile, reward


    def q(self, location, action=None):

        if state not in self.q_table:
            self.q_table[location] = np.zeros(len(self.actions))

        if action is None:
            return self.q_table[location]


        return q_table[location][action]



    def choose_action(self, player_state):
        if random.uniform(0, 1) < eps:
            return random.choice(self.actions)
        else:
            return np.argmax(q(player_state.location))

    def train_agent(self, player_state):

        for episode in range(N_EPISODES): 

            location = player_state.location
            total_reward = 0
            alpha = self.alphas[episode]

            for _ in range(MAX_EPISODE_STEPS):

                action = choose_action(player_state)
                next_location, reward = act(location, action)
                total_reward += reward 

                q(location)[action] = q(location, action) + \
                                      alpha * (reward + gamma * np.max(q(next_location)) - q(location, action))

                location = next_location     

            print(f"Episode {episode + 1}: total reward -> {total_reward}")


        return                  

    def next_move(self, game_state, player_state):
        train_agent(player_state)
        location = player_state.location
        action = np.argmax(qtable[location,:])
        print(action)
        return action