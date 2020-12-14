"""
TEMPLATE for creating your own Agent to compete in
'Dungeons and Data Structures' at the Coder One AI Sports Challenge 2020.
For more info and resources, check out: https://bit.ly/aisportschallenge

BIO:
Agent that values hunting the other player and killing them. Uses Q-Learning
to find the optimal strategy to achieve its goal.

"""

# import any external packages by un-commenting them
# if you'd like to test / request any additional packages - please check with the Coder One team
import random


# import time
# import numpy as np
# import pandas as pd
# import sklearn

class Agent:

    def __init__(self):
        """Place any initialisation code for your agent here (if any)"""
        pass

    def next_move(self, game_state, player_state):
        """This method is called each time your Agent is required to choose an action"""

        # a list of all the actions your Agent can choose from
        actions = ['', 'u', 'd', 'l', 'r', 'p']

        # randomly choosing an action
        action = random.choice(actions)

        return action
