# Binance Trading Bot
by _Manuel Velarde_

## Reference Links
- [Python Binance API Documentation](https://python-binance.readthedocs.io/en/latest/)
- [Python Binance API Repository](https://github.com/sammchardy/python-binance)
- [Binance Official API Documentation](https://github.com/binance/binance-spot-api-docs)
- [Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy](https://github.com/AI4Finance-LLC/Deep-Reinforcement-Learning-for-Automated-Stock-Trading-Ensemble-Strategy-ICAIF-2020)

## Markov Decision Process

The software focuses on the top cryptocurrencies with highest volume on Binance. The number of cryptocurrencies will be denoted by the letter `D`.

#### State
The state `s` consists of the list `[p, h, b]`. First, `p` denotes the prices in **USDT** in a matrix of floats with magnitude `5xD`. Each row contains the average over a different time range for each cryptocurrency. Second, `h` denotes the number of coins we hold for each cryptocurrency in a vector of floats with magnitude `D`. Finally, `b` denotes the balance in the **USDT** account as a float.

#### Action
The action `a` consists of a vector for the possible actions regarding each cryptocurrency that the agent can take. The vector will be `3xD` since the agent can _sell_, _hold_, or _buy_. The action can affect `h` and `b`.

#### Reward
The reward `r(s, a, next_s)` is the direct reward of taking the action `a` on the state `s` and arriving to the new state `next_s`.

#### Policy
The polict `pi(s)` represents the trading strategy at state `s`. This is the probability distribution of actions at the current state.

#### Value
The value `Q_pi(s, a)` represents the expected reward of taking action `a` at state `s` following the policy `pi`.

## Progress

### First Round
```
Episode 10      Last reward: -1.62      Average reward: 5.38    Time: 19
Episode 20      Last reward: -1.58      Average reward: 2.63    Time: 14
Episode 30      Last reward: -1.38      Average reward: 0.98    Time: 23
Episode 40      Last reward: -1.52      Average reward: 0.05    Time: 51
Episode 50      Last reward: -1.37      Average reward: -0.56   Time: 19
Episode 60      Last reward: -1.66      Average reward: -0.94
Episode 70      Last reward: -1.58      Average reward: -1.17
Episode 80      Last reward: -1.45      Average reward: -1.28
Episode 90      Last reward: -1.39      Average reward: -1.37
Episode 100     Last reward: -1.56      Average reward: -1.43
Episode 110     Last reward: -1.47      Average reward: -1.45
Episode 120     Last reward: -1.37      Average reward: -1.46
Episode 130     Last reward: -1.41      Average reward: -1.46
Episode 140     Last reward: -1.37      Average reward: -1.47
Episode 150     Last reward: -1.51      Average reward: -1.49
Episode 160     Last reward: -1.41      Average reward: -1.48
Episode 170     Last reward: -1.57      Average reward: -1.51
Episode 180     Last reward: -1.42      Average reward: -1.50
Episode 190     Last reward: -1.49      Average reward: -1.45
Episode 200     Last reward: -1.61      Average reward: -1.42
Episode 210     Last reward: -1.51      Average reward: -1.44
Episode 220     Last reward: -1.57      Average reward: -1.36
Episode 230     Last reward: -1.77      Average reward: -1.33
Episode 240     Last reward: 0.23       Average reward: -1.26
Episode 250     Last reward: -1.43      Average reward: -1.27
Episode 260     Last reward: -1.24      Average reward: -1.34
Episode 270     Last reward: -1.52      Average reward: -1.34
Episode 280     Last reward: -1.40      Average reward: -1.30
Episode 290     Last reward: -1.44      Average reward: -1.32
Episode 300     Last reward: -0.57      Average reward: -1.33
Episode 310     Last reward: -1.51      Average reward: -1.26
Episode 320     Last reward: -0.80      Average reward: -1.28
Episode 330     Last reward: 2.16       Average reward: -0.89
Episode 340     Last reward: -1.45      Average reward: -1.05
Episode 350     Last reward: -1.38      Average reward: -0.99
Episode 360     Last reward: 0.75       Average reward: -0.53
Episode 370     Last reward: -1.22      Average reward: -0.57
Episode 380     Last reward: -1.56      Average reward: -0.76
Episode 390     Last reward: -1.60      Average reward: -0.97
Episode 400     Last reward: -1.47      Average reward: -0.91
Episode 410     Last reward: -1.41      Average reward: -0.91
```