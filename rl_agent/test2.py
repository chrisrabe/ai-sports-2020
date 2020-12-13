import numpy as np

actions = ['', 'l', 'r', 'u', 'd', 'p']



# Initialise Q-table
state_size = 12000
action_size = len(actions)

qtable = np.zeros((8, 6))
print(qtable)

qtable[2][5] = 100

print(qtable)
print(np.argmax(qtable[2][:]))
# number = [[1, 3, 5, 7, 8],
# 		  [1, 3, 5, 19, 8]]
# print(np.argmax(number[0][:]))