# for the gym environment
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import gym
from gym import spaces
from binance.client import Client



# binance trading gym environment
class CryptoEnv(gym.Env):
    
    def __init__(self, api_key, secret_key, asset='BTC'):
        
        # for binance interaction
        self.client = Client(api_key, secret_key)
        self.asset = asset
        self.symbol = '{}USDT'.format(asset)
        
        # to plot progress
        self.episode = 1
        self.graph_reward = []
        self.graph_value = []
        self.graph_action = []

        # gym requirements
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            low=-np.pi,
            high=np.pi,
            shape=(25,),
            dtype=np.float16)
        
        # for state
        self.worth = None
        self.anchor = None
        self.anchor_base = None
        self.prev_price = None

        # TODO
        # self.prices = np.zeros((121,))
        self.prices = np.zeros((129,))

        self.asset_held = None
        self.asset_base = None
        self.usdt_held = None
        self.has = -1


    def reset(self, asset):

        # set asset
        self.asset = asset
        self.symbol = '{}USDT'.format(asset)
        self.asset_held = float(self.client.get_asset_balance(asset=self.asset)['free'])
        self.usdt_held = float(self.client.get_asset_balance(asset='USDT')['free'])

        # get velocities

        # TODO
        # for i in range(121):
        for i in range(129):

            self.prices[i] = float(self.client.get_symbol_ticker(symbol='BTCUSDT')['price'])
            time.sleep(1)

        # current worth
        state = self._next_observation()
        self.asset_base = self.prev_price
        self.worth = self.usdt_held + (self.asset_held * self.prev_price)
        self.anchor = self.worth
        self.anchor_base = self.anchor
        
        # print('RESET WITH {}'.format(self.asset))
        # print('HOLD: ', self.asset_held)
        # print('USDT: ', self.usdt_held)
        # print()

        # variables to track
        self.episode_reward = 0
        self.current_step = 1

        self.graph_reward = []
        self.graph_value = []
        self.graph_action = []

        return state

    
    def _next_observation(self):

        # get price
        price = float(self.client.get_symbol_ticker(symbol=self.symbol)['price'])

        # get new velocities
        self.prices = np.concatenate([self.prices[1:], np.array([price])])
        dx = np.array([1, 1, 1, 1, \
                       2, 2, 2, 2, \
                       4, 4, 4, 4, \
                       8, 8, 8, 8, \
                       16, 16, 16, 16, \
                       32, 32, 32, 32])
        dy = np.zeros((24,))
        for i in range(4):

            # TODO
            # dx = 5
            # dy[i] = self.prices[((i+1)*5)+100] - self.prices[(i*5)+100]
            # dx = 10
            # dy[i+4] = self.prices[((i+1)*10)+80] - self.prices[(i*10)+80]
            # dx = 20
            # dy[i+8] = self.prices[((i+1)*20)+40] - self.prices[(i*20)+40]
            # dx = 30
            # dy[i+12] = self.prices[(i+1)*30] - self.prices[i*30]
            # dx = 1
            dy[i] = self.prices[(i+1)+124] - self.prices[i+124]
            # # dx = 2
            dy[i+4] = self.prices[((i+1)*2)+120] - self.prices[(i*2)+120]
            # # dx = 4
            dy[i+8] = self.prices[((i+1)*4)+112] - self.prices[(i*4)+112]
            # # dx = 8
            dy[i+12] = self.prices[((i+1)*8)+96] - self.prices[(i*8)+96]
            # # dx = 16
            dy[i+16] = self.prices[((i+1)*16)+64] - self.prices[(i*16)+64]
            # # dx = 16
            dy[i+20] = self.prices[(i+1)*32] - self.prices[i*32]

        # TODO
        arctan = np.arctan(dy/dx)
        observation = np.concatenate([arctan, np.array([self.has])])

        self.prev_price = price

        # TODO
        # return arctan
        return observation

    
    def step(self, action):

        self.current_step += 1
        prev_worth = self.worth
        self._take_action(action)
        state = self._next_observation()
        self.worth = self.usdt_held + (self.asset_held * self.prev_price)
        reward = self.worth - prev_worth
        self.episode_reward += reward
        # if reward < 0:
        #     reward *= 2

        # print('STEP', self.current_step-1, reward)
        
        self.graph_reward.append(reward)
        self.graph_value.append((self.prev_price - self.asset_base) / self.asset_base * 100)

        done = False
        if self.worth > self.anchor * 1.001:
            self.anchor = self.anchor * 1.001
            if self.worth > self.anchor_base * 1.01:
                done = True
            # reward *= 10
        elif self.worth < self.anchor * 0.995:
            done = True
        
        return state, reward, done, {}

    
    def _take_action(self, action):
        
        action = int(action)
        price = float(self.client.get_symbol_ticker(symbol=self.symbol)['price'])
        
        if action == 0:
            # print('BUY')
            self.graph_action.append(1)
            if self.usdt_held > 0.0:
                self.has = 1
                self.asset_held += ((self.usdt_held * .999) / price)
                self.usdt_held = 0.0

        if action == 1:
            # print('SELL')
            self.graph_action.append(-1)
            if self.asset_held > 0.0:
                self.has = -1
                self.usdt_held += ((self.asset_held * price) * .999)
                self.asset_held = 0.0
        
        # if action == 1:
        #     self.graph_action.append(0)

    
    def plot_progress(self):
        x_axis = list(range(1, self.current_step))
        # print(self.graph_reward)
        # print(np.cumsum(self.graph_reward))
        # print(x_axis)
        cumulative = np.cumsum(self.graph_reward)
        maximum = abs(max(cumulative))
        minimum = abs(min(cumulative))
        self.graph_action = np.array(self.graph_action)
        self.graph_action = self.graph_action * max(maximum, minimum)
        plt.plot(x_axis, self.graph_value, label='Asset Price Change')
        plt.plot(x_axis, np.cumsum(self.graph_reward), label='Cumulative Reward')
        plt.plot(x_axis, self.graph_action, label='Action Taken')
        plt.title('Episode {} with {}'.format(self.episode, self.asset))
        plt.xlabel('Number of Steps')
        plt.ylabel('Value in Dollars')
        plt.legend()
        plt.savefig('images/ep{}.png'.format(self.episode))
        plt.clf()
        self.episode += 1


    def set_epoch(self, epoch):
        self.episode = epoch