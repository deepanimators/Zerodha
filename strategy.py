# -*- coding: utf-8 -*-
"""
Created on Sat Jun 06 22:27:19 2024

@author: deepak
File Name: strategy.py
"""

from kiteconnect import KiteConnect
import os
import pandas as pd
import time
import traceback
from utils import notify, buy_nearest_option, sell_option, update_positions, get_initial_price, getTickSize
from access_token import autologin
import sys

cwd = os.getcwd()

autologin()

# creating trading session
access_token = open("access_token.txt", 'r').read()
key_secret = open("api_key.txt", 'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

# Load values from prerequisite Excel sheet
excel_file_prerequisite = 'prerequisite.xlsx'
prerequisite_df = pd.read_excel(excel_file_prerequisite)

tickers = prerequisite_df['Tickers'].tolist()
LOT_SIZE = prerequisite_df['Lotsize'].iloc[0]
n_shares = prerequisite_df['nShares'].iloc[0]
capital = prerequisite_df['Capital'].iloc[0]

quantity = int(n_shares * LOT_SIZE)  # Ensure quantity is an integer

exchange_type = kite.EXCHANGE_NSE
NSE_NFO = "NSE"
if NSE_NFO == "NFO":
    exchange_type = kite.EXCHANGE_NFO

product_type = kite.PRODUCT_MIS

# get dump of all nfo instruments
instrument_dump = kite.instruments(NSE_NFO)
instrument_df = pd.DataFrame(instrument_dump)

# Load fixed levels from Excel sheet
excel_file = 'fixed_levels.xlsx'
fixed_levels_df = pd.read_excel(excel_file)
fixed_levels = fixed_levels_df['Levels'].tolist()


def main(ticker, initial_price):

    print("\n**************************************************************")
    print("starting passthrough for {} at {}".format(ticker, time.asctime(time.localtime(time.time()))))

    try:
        ltp = kite.ltp(NSE_NFO + ':' + ticker)[NSE_NFO + ':' + ticker]['last_price']
        tick_size = getTickSize(instrument_df, ticker)

        print("Current Price - ", ltp)
        print("Initial Price - ", initial_price)

        # Entry strategy
        for i, level in enumerate(fixed_levels):
            if i % 2 == 0:  # Even-numbered levels (entry values)
                if initial_price > level and ltp >= level:
                        # Entry condition for selling put
                        sell_option(kite, ticker, quantity, exchange_type, product_type, option_type='PE')
                        # Set target and stop loss with odd numbered values
                        target = next((x for x in fixed_levels if x > level and x % 2 != 0), level + 1)
                        stop_loss = next((x for x in fixed_levels if x < level and x % 2 != 0), level - 1)
                        # Purchase nearest Rs. 10 call
                        buy_nearest_option(kite, ticker, ltp, quantity, exchange_type, product_type, option_type='CE',
                                           target=target, stop_loss=stop_loss)
                        update_positions(kite,ticker)
                        break
                elif initial_price < level and ltp <= level:
                        # Entry condition for selling call
                        sell_option(kite, ticker, quantity, exchange_type, product_type, option_type='CE')
                        # Set target and stop loss
                        target = next((x for x in fixed_levels if x < level and x % 2 != 0), level - 1)
                        stop_loss = next((x for x in fixed_levels if x > level and x % 2 != 0), level + 1)
                        # Purchase nearest Rs. 10 put
                        buy_nearest_option(kite, ticker, ltp, quantity, exchange_type, product_type, option_type='PE',
                                           target=target, stop_loss=stop_loss)
                        update_positions(ticker)
                        break

    except Exception:
        notify(error=True)
        print("API error for ticker :", ticker)
        print(traceback.format_exc())


start_time = time.time()
timeout = time.time() + 60 * 60 * 6  # 60 seconds times 360 meaning 6 hrs


initial_prices = {}
for ticker in tickers:
    initial_prices[ticker] = kite.ltp(NSE_NFO + ':' + ticker)[NSE_NFO + ':' + ticker]['last_price']


while time.time() <= timeout:
    try:
        for ticker in tickers:
            main(ticker, initial_prices[ticker])
            # Check the price every 3 minutes 
        print("Sleeping for ", max(0, int(180 - ((time.time() - start_time) % 180))))
        time.sleep(max(0, int(180 - ((time.time() - start_time) % 180))))
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        sys.exit()
