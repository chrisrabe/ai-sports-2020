import gym
import numpy as np
import random
import os
from time import sleep
class bcolors:
    RED= '\u001b[31m'
    GREEN= '\u001b[32m'
    RESET= '\u001b[0m'
# Create an instance of the 'Taxi' environment
env = gym.make('Taxi-v3')
# Initialise Q-table
state_size = env.observation_space.n
action_size = env.action_space.n
qtable = np.zeros((state_size, action_size))
# Hyperparameters 
learning_rate = 0.9
discount_rate = 0.8
epsilon = 1.0
decay_rate = 0.01 
# Variables controlling how long our agent will train for
num_episodes = 1000
num_steps = 99
print("AGENT IS TRAINING...")
for episode in range(num_episodes):
    # Reset the environment
    state = env.reset()
    step = 0
    done = False
 	
    print((state))


    for step in range(num_steps):
        # Exploration-exploitation tradeoff
        if random.uniform(0,1) < epsilon:
            # Explore
            action = env.action_space.sample()
        else:
            # Exploit
            action = np.argmax(qtable[state,:])
        # Take an action and observe the reward
        new_state, reward, done, info = env.step(action)
        # Q-learning algorithm
        qtable[state,action] = qtable[state,action] + learning_rate * (reward + discount_rate * np.max(qtable[new_state,:]) - qtable[state,action])
        # Update to our new state
        state = new_state
        # if done, finish episode
        if done == True:
            break
    # Decrease epsilon
    epsilon = np.exp(-decay_rate*episode)
 
# Get ready to watch our trained agent
os.system('cls')
print(qtable)
print(f"Training completed over {num_episodes} episodes")
input("Press Enter to see our trained agent play")
sleep(1)
os.system('cls')  
episodes_to_preview = 3
for episode in range(episodes_to_preview):
    # Reset the environment
    state = env.reset()
    step = 0
    done = False
    episode_rewards = 0
    for step in range(num_steps):
        # clear screen
        os.system('cls')
        print(f"TRAINED AGENT")
        print("+++++EPISODE {}+++++".format(episode+1))
        print("Step {}".format(step+1))
        # Exploit
        action = np.argmax(qtable[state,:])
        # Take an action and observe the reward
        new_state, reward, done, info = env.step(action)
        # Accumulate our rewards    
        episode_rewards += reward
        env.render()
        print("")
        if episode_rewards < 0:
            print(f"Score: {bcolors.RED}{episode_rewards}{bcolors.RESET}")
        else:
            print(f"Score: {bcolors.GREEN}{episode_rewards}{bcolors.RESET}")
        sleep(0.5)   
 
        # Update to our new state
        state = new_state
        # if done, finish episode
        if done == True:
            break 
# Close the Taxi environment
env.close()