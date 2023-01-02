import os
import datetime
import pandas as pd
from eod import EodHistoricalData

last_day = datetime.date.today()
first_day = last_day - datetime.timedelta(days=7)


def build_connection():
    key = os.environ["API_EOD"]
    client = EodHistoricalData(key)
    return client


class CheckForOpportunity():

    def __init__(self,
                 symbol,
                 buy_signal,
                 sell_signal):

        self.symbol = symbol
        self.buy_signal = buy_signal
        self.sell_signal = sell_signal

    def get_data(self, symbol):
        client = build_connection()
        prices = client.get_prices_eod(symbol,
                                       period="d",
                                       order="a",
                                       from_=first_day,
                                       to=last_day)

        return pd.DataFrame(prices)


#    def calculate_average(self, data):
