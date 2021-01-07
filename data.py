# code by Manuel Velarde da Silva

import os
import time
import datetime
import numpy as np
from dotenv import load_dotenv
from binance.client import Client
from twisted.internet import reactor
from binance.websockets import BinanceSocketManager



# load environment variables
load_dotenv()
API = os.getenv('API_KEY')
SECRET = os.getenv('SECRET_KEY')
CLIENT = Client(API, SECRET)
BINANCE = BinanceSocketManager(CLIENT)

# symbols to track
SYMBOLS = ['BTC', 'ETH', 'GRT', 'XRP', 'LTC', 'BCH', 'BNB' ]
COUNTER = 0

# state representation
D = len(SYMBOLS)
p = np.zeros((D * 3,))  # 3 features per symbol



# to handle market stream
def handler(msg):
    global p
    global SYMBOLS
    global COUNTER
    # get symbol location
    symbol = msg['s'][:-4]
    i = SYMBOLS.index(symbol) * 3
    # get features
    price = msg['c']
    yesterday_price = msg['x']
    volume = msg['v']
    p[i] = price
    p[i+1] = yesterday_price
    p[i+2] = volume
    # increase counter
    COUNTER += 1
    # print("{} {} {} {}".format(symbol, price, yesterday_price, volume))
    if COUNTER == len(SYMBOLS):
        global CLIENT
        # build state representation h
        h = np.zeros(8,)
        for j in range(COUNTER):
            h[j] = float(CLIENT.get_asset_balance(asset=SYMBOLS[j])['free'])
        # build state representation b
        h[7] = float(CLIENT.get_asset_balance(asset='USDT')['free'])
        COUNTER = 0
        s = np.concatenate([p, h])
        print(s)
        print()
        # send state representation to RL agent


# to sell at market price
def sell(coin, client, test=True):
    coin_balance = client.get_asset_balance(asset=coin)
    quantity = '{:0.0{}f}'.format(float(coin_balance['free']), 3)
    symbol = '{}USDT'.format(coin)
    if test:
        order = client.create_test_order(
            symbol=symbol,
            side=client.SIDE_SELL,
            type=client.ORDER_TYPE_MARKET,
            quantity=quantity)
        status = 'TEST'
    else:
        order = client.order_market_sell(
            symbol=symbol,
            quantity=quantity)
        status = order['status']
    print('SELL {} {} {}'.format(coin, quantity, status))


# to buy at market price
def buy(coin, client, test=True):
    usd_balance = client.get_asset_balance(asset='USDT')
    available_usd = min(float(usd_balance['free']) * 0.9, 1000)
    price = float(client.get_avg_price(symbol='{}USDT'.format(coin))['price'])
    quantity = '{:0.0{}f}'.format(available_usd / price, 3)
    symbol = '{}USDT'.format(coin)
    if test:
        order = client.create_test_order(
            symbol=symbol,
            side=client.SIDE_BUY,
            type=client.ORDER_TYPE_MARKET,
            quantity=quantity)
        status = 'TEST'
    else:
        order = client.order_market_buy(
            symbol=symbol,
            quantity=quantity)
        status = order['status']
    print('BUY {} {} {}'.format(coin, quantity, status))



def get_macd(client, asset):
    weight_25 = [0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07, 1.08, 1.09, 1.10, 1.11, 1.12]
    kline_25 = CLIENT.get_historical_klines("{}USDT".format(asset), Client.KLINE_INTERVAL_5MINUTE, "125 min ago UTC")
    total_25 = 0
    weight_11 = weight_25[7:18]
    kline_11 = kline_25[-11:]
    total_11 = 0
    for i in range(25):
        temp = float(kline_25[i][4]) * weight_25[i]
        total_25 += temp
    total_25 /= 25
    for i in range(11):
        temp = float(kline_11[i][4]) * weight_11[i]
        total_11 += temp
    total_11 /= 11
    return total_11 - total_25


def main(test=True):

    # define variables
    global SYMBOLS
    global CLIENT
    global BINANCE

    price = float(CLIENT.get_symbol_ticker(symbol='BTCUSDT')['price'])
    print('CURRENT PRICE', price)
    print()
    print(CLIENT.get_asset_balance(asset='USDT'))
    print(CLIENT.get_asset_balance(asset='BTC'))
    print()

    prices = np.zeros((121,))
    for i in range(121):
        prices[i] = float(CLIENT.get_symbol_ticker(symbol='BTCUSDT')['price'])
        time.sleep(1)
    print(prices)
    dx = np.array([5, 5, 5, 5, 10, 10, 10, 10, 20, 20, 20, 20, 30, 30, 30, 30])
    dy = np.zeros((16,))
    for i in range(4):
        # dx = 5
        dy[i] = prices[((i+1)*5)+100] - prices[(i*5)+100]
        # dx = 10
        dy[i+4] = prices[((i+1)*10)+80] - prices[(i*10)+80]
        # dx = 20
        dy[i+8] = prices[((i+1)*20)+40] - prices[(i*20)+40]
        # dx = 30
        dy[i+12] = prices[(i+1)*30] - prices[i*30]
    arctan = np.arctan(dy/dx)
    print(arctan.dtype)
    print(arctan)

    
    # # setup connections
    # connections = {}
    # for s in SYMBOLS:
    #     ticker = '{}USDT'.format(s)
    #     connections[s] = BINANCE.start_symbol_ticker_socket(ticker, handler)

    # # get the data
    # BINANCE.start()
    # time.sleep(10)

    # # close connections
    # for s in SYMBOLS:
    #     BINANCE.stop_socket(connections[s])
    
    # # disconnect from crypto exchange
    # reactor.stop()
    # BINANCE.close()



if __name__ == '__main__':
    main()