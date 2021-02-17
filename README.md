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
