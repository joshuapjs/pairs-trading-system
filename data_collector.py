from build_connection import build_connection
import pandas as pd
import datetime
import os

api_key = os.environ["API_EOD"]

# Calculating three different dates for defining the relevant lengths of the time series
today = datetime.date.today()
seven_days = today - datetime.timedelta(days=7)
two_hundred_days = today - datetime.timedelta(days=200)
five_years_ago = today - datetime.timedelta(days=365 * 5)


def currency_intraday(currency_pair, start_date, pricing_interval: str):

    def to_epoch(time_stamp):
        epoch_stamp = (pd.Timestamp(time_stamp) - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")
        return epoch_stamp

    client = build_connection()
    exchange_rates = pd.DataFrame(client.get_prices_intraday(currency_pair + '.FOREX',
                                                             interval=pricing_interval,
                                                             _from=to_epoch(start_date),
                                                             to=to_epoch(today)))

    return exchange_rates


# Method to request stock prices for a specific period
def close_data(symbol, start_date):

    client = build_connection()
    prices = client.get_prices_eod(symbol,
                                   period="d",
                                   order="a",
                                   from_=start_date,
                                   to=today)

    return pd.DataFrame(prices).set_index("date")
