# from local files
import agent
import environment

# from libraries
import os
import random
from itertools import count
from dotenv import load_dotenv


# load binance keys
load_dotenv()
API = os.getenv('API_KEY')
SECRET = os.getenv('SECRET_KEY')
assets = ['BTC', 'ETH', 'BCH']

# agent constants
GAMMA = 0.99
LOG_INTERVAL = 10


env = environment.CryptoEnv(API, SECRET)
model = agent.Policy()
optimizer = agent.optim.Adam(model.parameters(), lr=3e-2)

running_reward = 10

# to load checkpoint
episode_start = 1
LOAD = False

if LOAD:
    checkpoint = agent.load_progress(episode_start-1)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    env.set_epoch(checkpoint['epoch']+1)
    episode_start = checkpoint['epoch']+1
    running_reward = checkpoint['reward']


# run inifinitely many episodes
for i_episode in count(episode_start):

    # reset environment and episode reward
    state = env.reset(random.choice(assets))
    ep_reward = 0

    # for each episode, only run 9999 steps so that we don't 
    # infinite loop while learning
    for t in range(1, 10000):

        # select action from policy
        action = agent.select_action(model, state)

        # take the action
        state, reward, done, _ = env.step(action)

        model.rewards.append(reward)
        ep_reward += reward
        if done:
            break

    # plot progress
    env.plot_progress()

    # update cumulative reward
    running_reward = 0.05 * ep_reward + (1 - 0.05) * running_reward

    # perform backprop
    agent.finish_episode(model, optimizer, GAMMA)

    # log results
    if i_episode % LOG_INTERVAL == 0:
        agent.save_progress(model, optimizer, i_episode, running_reward)
        print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'.format(
                i_episode, ep_reward, running_reward))

    # check if we have "solved" the cart pole problem
    # if running_reward > env.spec.reward_threshold:
    #     print("Solved! Running reward is now {} and "
    #           "the last episode runs to {} time steps!".format(running_reward, t))
    #     break