import numpy as np

from build_connection import build_connection
from data_grabber import real_time_data
from scipy import stats
import datetime
import pandas as pd


# Calculating three different dates for defining the relevant lengths of the series
last_day = datetime.date.today()
start_short_period = last_day - datetime.timedelta(days=7)
start_long_period = last_day - datetime.timedelta(days=200)


# Method to request stock prices for a specific period
def get_data(symbol, current_date):
    client = build_connection()
    prices = client.get_prices_eod(symbol,
                                   period="d",
                                   order="a",
                                   from_=current_date,
                                   to=last_day)

    return pd.DataFrame(prices).set_index("date")


# Class to create signals for buying or selling a stock
class CheckForOpportunity:

    def __init__(self,
                 symbol,
                 buy_signal=False,
                 sell_signal=False):

        self.symbol = symbol
        self.buy_signal = buy_signal
        self.sell_signal = sell_signal

# Method to set a buy or sell signal depending on the kind of trend
    def get_technical_trend(self):
        long_period = get_data(self.symbol, start_long_period)
        short_period = long_period[str(start_short_period):]
        long_average = long_period["adjusted_close"].mean()
        short_average = short_period["adjusted_close"].mean()

        if long_average < short_average:
            self.buy_signal = True
        else:
            self.sell_signal = True

        output = {"buy_signal": self.buy_signal,
                  "sell_signal": self.sell_signal}

        return output

    def short_term_trend(self):
        data = real_time_data()
        delta = (data.index - data.index[0])
        days = delta.seconds
        result = stats.linregress(days, data["Ask"])
        print(result.slope)

        return data
