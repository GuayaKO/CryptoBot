import os
import time
import copy
import datetime
import pandas as pd
from dotenv import load_dotenv
from binance.client import Client
from twisted.internet import reactor
from binance.websockets import BinanceSocketManager



# load environment variables
load_dotenv()
API = os.getenv('API_KEY')
SECRET = os.getenv('SECRET_KEY')



def create_structure(symbols):
    row = {}
    row['event_time'] = 0
    cols = ['event_time']
    for s in symbols:
        row['{}_market'.format(s)] = 0
        cols.append('{}_market'.format(s))
        row['{}_price'.format(s)] = 0.0
        cols.append('{}_price'.format(s))
        row['{}_quantity'.format(s)] = 0.0
        cols.append('{}_quantity'.format(s))
    return pd.DataFrame(columns=cols), row



# create data structures
SYMBOLS = ['XLM', 'XRP', 'BTC', 'ETH', 'LINK', 'ADA', \
           'LTC', 'BCH', 'BNB', 'EOS', 'TRX', 'VET', \
           'DASH', 'ETC', 'XMR']
STRUCTURE, ROW = create_structure(SYMBOLS)



def handle_stream(msg):

    # define variables
    global STRUCTURE
    global SYMBOLS
    symbol = msg['s'][:-4]
    price = msg['p']
    quantity = msg['q']
    market = 1 if msg['m'] else -1
    event_time = msg['E']
    event = STRUCTURE.index[STRUCTURE['event_time'] == event_time].tolist()

    # add data to structure
    if event:
        STRUCTURE.at[event[0], '{}_quantity'.format(symbol)] += float(quantity)
        STRUCTURE.at[event[0], '{}_price'.format(symbol)] = float(price)
        STRUCTURE.at[event[0], '{}_market'.format(symbol)] += market
    else:
        row = copy.deepcopy(ROW)
        row['event_time'] = event_time
        row['{}_market'.format(symbol)] = market
        row['{}_price'.format(symbol)] = float(price)
        row['{}_quantity'.format(symbol)] = float(quantity)
        STRUCTURE = STRUCTURE.append(row, ignore_index=True)
    
    # save structure as CSV
    # if len(STRUCTURE.index) == 100:
    #     now = datetime.datetime.now()
    #     filename = now.strftime("%Y-%m-%d-%H-%M-%S")
    #     STRUCTURE.to_csv('./data/{}.csv'.format(filename))
    #     STRUCTURE, _ = create_structure(SYMBOLS)



def main():

    # define variables
    global SYMBOLS

    # connect to crypto exchange
    binance = BinanceSocketManager(Client(API, SECRET))

    # setup connections
    connections = {}
    for s in SYMBOLS:
        connections[s] = binance.start_trade_socket('{}USDT'.format(s), handle_stream)

    # get the data
    binance.start()
    time.sleep(3600)

    # close connections
    for s in SYMBOLS:
        binance.stop_socket(connections[s])
    
    # disconnect from crypto exchange
    reactor.stop()
    binance.close()

    # save the data
    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d-%H-%M-%S")
    STRUCTURE.to_csv('./data/{}.csv'.format(filename), index=False)



if __name__ == '__main__':
    main()