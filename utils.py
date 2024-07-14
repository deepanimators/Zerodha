# -*- coding: utf-8 -*-
"""
Created on Sat Jun 06 22:27:19 2024

@author: deepak
File Name: utils.py
"""

import traceback
import pandas as pd
import time
from termcolor import colored


def notify(error=False):
    """Make sound to notify"""
    import winsound
    frequency = 500  # Set Frequency To 500 Hertz
    duration = 200 if not error else 100  # Set Duration To 200 ms (or 100 ms for error)
    winsound.Beep(frequency, duration)


def placeMarketOrder(kite, symbol, buy_sell, quantity, exchange, product_type):
    """Places a Market order"""
    notify()
    order_type = "buy" if buy_sell == "buy" else "sell"
    print(colored(f"{symbol} - Placing Market {order_type} order at {time.asctime(time.localtime(time.time()))}",
                  'cyan' if buy_sell == 'buy' else 'yellow', 'on_grey'))
    t_type = kite.TRANSACTION_TYPE_BUY if buy_sell == "buy" else kite.TRANSACTION_TYPE_SELL

    kite.place_order(tradingsymbol=symbol, exchange=exchange, transaction_type=t_type, quantity=quantity,
                     order_type=kite.ORDER_TYPE_MARKET, product=product_type, variety=kite.VARIETY_REGULAR)


def sell_option(kite, ticker, quantity, exchange, product_type, option_type):
    # Construct the option symbol
    strike_price = 16000  # Example strike price; modify based on your logic
    option_ticker = construct_option_symbol(ticker, strike_price, option_type)
    placeMarketOrder(kite, option_ticker, "sell", quantity, exchange, product_type)


def buy_nearest_option(kite, ticker, ltp, quantity, exchange, product_type, option_type, target, stop_loss):
    # Construct the nearest option symbol
    nearest_option_ticker = construct_nearest_option_symbol(ticker, ltp, option_type)
    placeMarketOrder(kite, nearest_option_ticker, "buy", quantity, exchange, product_type)
    print(f"Bought {nearest_option_ticker} with target {target} and stop loss {stop_loss}")


def construct_option_symbol(ticker, strike_price, option_type):
    expiry = "24JUL2024"  # Update to the correct expiry date
    return f"{ticker}{expiry}{strike_price}{option_type}"


def construct_nearest_option_symbol(ticker, ltp, option_type):
    # Find the nearest Rs. 10 strike price
    nearest_strike = round(ltp / 10) * 10
    nearest_strike = int(nearest_strike)  # Ensure nearest_strike is an integer
    expiry = "24JUL2024"  # Update to the correct expiry date
    return f"{ticker}{expiry}{nearest_strike}{option_type}"


def update_positions(kite,ticker):
    try:
        positions = kite.positions()["day"]
        for position in positions:
            if position['tradingsymbol'] == ticker:
                print(f"Position for {ticker}:")
                print(f"Quantity: {position['quantity']}")
                print(f"Average Price: {position['average_price']}")
                print(f"Last Price: {position['last_price']}")
                print("---------------------------")
                break
    except Exception as e:
        notify(error=True)
        print(f"Error fetching positions for {ticker}: {e}")
        print(traceback.format_exc())


def getTickSize(instrument_df, symbol):
    """Gets the tick size for a given script from instrument dump"""
    try:
        return instrument_df[instrument_df.tradingsymbol == symbol].tick_size.values[0]
    except:
        return -1


def get_initial_price(kite, exchange, ticker):
    # Wait until 9:29 AM to fetch the initial price
    target_time = "09:29"
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == target_time:
            return kite.ltp(exchange + ':' + ticker)[exchange + ':' + ticker]['last_price']
        time.sleep(1)
