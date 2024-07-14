# Python-Zerodha-Trading

This repository contains sample templates for implementing trading strategies in Python using Zerodha's KiteConnect API.

## Zerodha KiteConnect
To understand the login process and other related functionalities, refer to the following links:

1. [KiteConnect API Documentation](https://kite.trade/docs/connect/v3/)
2. [KiteConnect Python Documentation](https://kite.trade/docs/pykiteconnect/v3/)
3. [KiteConnect Developer Login](https://developers.kite.trade/login)
4. [KiteConnect Developer Forum](https://kite.trade/forum/)

## Installation of Dependencies
Run the following command to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

1. In every 3 min candle, first the price for the ticker is fetched and the data will be captured in a dataframe. afterwhich the data will be checked with the fixed_levels.xlsx sheet based on the ohlc data fetched. Even values from the sheet will be taken as target position based on the ohlc data fetched. Once the ticker ohlc data is crossed or touched the value of the targeted even number value Above the ohlc start value the put value sells the lot selected and make the odd above value as target and below odd value as stop loss and make a purchase of any nearest Rs. 10 call value of the ticker. if the targeted even number value is below the ohlc start value the call value sells the lot selected and make the odd below value as target and above odd value as stop loss and make a purchase of any nearest Rs. 10 put value of the ticker.

FeedBack:
In every 3 min candle, first the ohlc data for the ticker is fetched and the data will be captured in a Data frame-

SRIKANTH - NO , by 9:29 get the price and after that no need of any candle timeframe , if price cross Even on up side then upside odd is target and downside odd is stop loss 

 2) After which the data will be checked with the fixed_levels.xlsx sheet based on the ohlc data fetched. Even values from the sheet will be taken as target position based on the ohlc data fetched

SRIKANTH - NO , Even values are for entry only , only odd are target 


3. Once the ticker ohlc data is crossed or touched the value of the targeted even number value Above the ohlc start value the put value sells the lot selected and make the odd above value as target and below odd value as stop loss 
SRIKANTH - yes correct , let’s call even value as entry value to avoid confusion 

4. and make a purchase of any nearest Rs. 10 call value of the ticker. if the targeted even number value is below the ohlc start value the call value sells the lot selected and make the odd below value as target and above odd value as stop loss and make a purchase of any nearest Rs. 10 put value of the ticker.
SRIKANTH - Yes right …


## Strategy for the workflow....

First, the current price for the ticker is fetched. After which the data will be checked with the fixed_levels.xlsx sheet based on the ticker price fetched. 
Even values from the sheet will be taken as nearest entry level based on the starting ticker price fetched. 
Take the above and below even numbers as target and stop loss point based on the even value selected. 

Once the ticker price is reaches or touches the value of the targeted even level value the put value sells the lot selected and make the odd above value of the targeted value as target and below odd value of the targeted value as stop loss and make a purchase of any nearest Rs. 10 call value of the ticker. 

If the ticker price is reaches or touches the value of the stop loss even level value and is below the entry start value the call value sells the lot selected and make the odd below value as target and above odd value as stop loss and make a purchase of any nearest Rs. 10 put value of the ticker. 

Below scenario as loop (Check the price every 3 minutes):
"wait until the current price reaches the targeted even numbers and stop loss point based on the even value captured. Once the ticker price is reaches or touches the value of the targeted even level value the put value sells the lot selected and make the odd above value of the targeted value as target and below odd value of the targeted value as stop loss and make a purchase of any nearest Rs. 10 call value of the ticker. 

If the  ticker price is reaches or touches the value of the stop loss even level value and is below the entry start value the call value sells the lot selected and make the odd below value as target and above odd value as stop loss and make a purchase of any nearest Rs. 10 put value of the ticker."


## Automating the Login Process

### For First-Time Setup

1. Install Selenium:

   ```bash
   pip install selenium
   ```

2. Download the correct webdriver from [https://developer.chrome.com/docs/chromedriver/downloads](https://developer.chrome.com/docs/chromedriver/downloads) and place the `.exe` file in the directory containing `access_token.py`.
3. Create an `api_key.txt` file with the following information:
   - API KEY: Obtained from the trading app in your developer account.
   - API SECRET: Obtained from the trading app in your developer account.
   - USER ID: Zerodha Kite user ID.
   - PASSWORD: Zerodha Kite password.
   - PIN: Zerodha Kite pin.

4. Run the following command:

   ```bash
   python strategy.py
   ```

## Strategy
The strategy implemented here involves buying when the indicator crosses below the candle and selling when the Indicator crosses above the candle. The strategy code is in `strategy.py`, and additional utility functions are in `utils.py`.

## Daily Usage

It is recommended to adjust the global variables in `strategy.py` and fixed values in `fixed_levels.xlsx` based on the even targets to align with your new strategy. Additionally, run `strategy.py` one minute after the candle start time (for larger duration candles like 15 minutes or longer). For example, if you want to start at 9:15 AM, run the code at 9:16 AM to avoid missing some signals.

1. Run:

   ```bash
   python strategy.py
   ```
