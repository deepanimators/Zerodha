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


## Automating the Login Process

### For First-Time Setup

1. Install Selenium included in requirements.txt file:

   ```bash
   pip install -r requirements.txt
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

## Strategy for the workflow....

The strategy implemented here involves buying when the indicator crosses below the candle and selling when the Indicator crosses above the candle. The strategy code is in `strategy.py`, and additional utility functions are in `utils.py`.

First, the current price for the ticker is fetched. After which the data will be checked with the fixed_levels.xlsx sheet based on the ticker price fetched. 
Even values from the sheet will be taken as nearest entry level based on the starting ticker price fetched. 
Take the above and below even numbers as target and stop loss point based on the even value selected. 

Once the ticker price is reaches or touches the value of the targeted even level value the put value sells the lot selected and make the odd above value of the targeted value as target and below odd value of the targeted value as stop loss and make a purchase of any nearest Rs. 10 call value of the ticker. 

If the ticker price is reaches or touches the value of the stop loss even level value and is below the entry start value the call value sells the lot selected and make the odd below value as target and above odd value as stop loss and make a purchase of any nearest Rs. 10 put value of the ticker. 

Below scenario as loop (Check the price every 3 minutes):
"wait until the current price reaches the targeted even numbers and stop loss point based on the even value captured. Once the ticker price is reaches or touches the value of the targeted even level value the put value sells the lot selected and make the odd above value of the targeted value as target and below odd value of the targeted value as stop loss and make a purchase of any nearest Rs. 10 call value of the ticker. 

If the  ticker price is reaches or touches the value of the stop loss even level value and is below the entry start value the call value sells the lot selected and make the odd below value as target and above odd value as stop loss and make a purchase of any nearest Rs. 10 put value of the ticker."



## Daily Usage

It is recommended to adjust the global variables in `prerequisite.xlsx` and fixed values in `fixed_levels.xlsx` based on the even targets to align with your new strategy. Additionally, run `strategy.py` one minute after the candle start time (for larger duration candles like 3 minutes or longer). For example, if you want to start at 9:15 AM, run the code at 9:16 AM to avoid missing some signals.

1. Run:

   ```bash
   python strategy.py
   ```
