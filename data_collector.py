from websocket import create_connection
from build_connection import build_connection
import pandas as pd
from io import StringIO
from scipy import stats
import requests
import datetime
import time
import json
import os

api_key = os.environ["API_EOD"]

# Calculating three different dates for defining the relevant lengths of the series
last_day = datetime.date.today()
start_short_period = last_day - datetime.timedelta(days=7)
start_long_period = last_day - datetime.timedelta(days=200)


# Infinite loop waiting for WebSocket data
def init_real_time(symbol):

    ask = []
    bid = []
    timestamp = []

    # Connect to WebSocket API and subscribe to trade feed for a stock symbol
    ws = create_connection(f"wss://ws.eodhistoricaldata.com/ws/crypto?api_token={api_key}")
    ws.send(f'{{"action": "subscribe", "symbols": "{symbol}"}}')

    # Collecting initial data points für real_time_data
    while True:
        if len(ask) < 10:
            result = ws.recv()
            result = json.loads(result)
            if len(result) > 2:
                ask.append(result["ap"])
                bid.append(result["bp"])
                timestamp.append(datetime.datetime.fromtimestamp(result["t"]/1000.0))
                time.sleep(1)
        else:
            prices = pd.DataFrame({"Ask": ask, "Bid": bid, "Time": timestamp})  # adding bid, ask and time to a df
            ask.clear()
            bid.clear()
            timestamp.clear()
            prices.index = prices["Time"]
            del prices["Time"]
            return prices


def real_time_data(symbol):

    # Connect to WebSocket API and subscribe to trade feed for Ethereum and Bitcoin - will be replaced by stock prices
    ws = create_connection(f"wss://ws.eodhistoricaldata.com/ws/crypto?api_token={api_key}")
    ws.send(f'{{"action": "subscribe", "symbols": "{symbol}"}}')

    df = init_real_time(symbol).copy()

    # collecting additional data points for the symbol given
    while True:
        result = ws.recv()
        result = json.loads(result)
        if len(result) > 2:
            while True:
                result = ws.recv()
                result = json.loads(result)
                ask = result["ap"]
                bid = result["bp"]
                timestamp = datetime.datetime.fromtimestamp(result["t"] / 1000.0)
                df.loc[timestamp] = [ask, bid]
                # If maximum number of rows are exceeded by one, one old datapoint will be deleted
                if len(df["Ask"]) > 10:
                    df.drop(index=df.index[0], axis=0, inplace=True)
                # Getting the trend by running a regression on the rolling datapoints
                result = stats.linregress(range(len(df["Ask"])), df["Ask"].astype(float))
                print(result.slope)  # modification needed - data should be stored in a database
                time.sleep(1)


def intraday_data(symbol, start, end, interval="1m"):
    """
    :param symbol: ticker symbol of a US Stock
    :param start: required datetime.datetime object e.g. datetime.datetime(2022, 1, 10, 15, 10, 0)
    :param end: required Format datetime.datetime object e.g. datetime.datetime(2022, 1, 10, 16, 0, 0)
    :param interval: either 1m (standard) or 5m
    :return: DataFrame
    """

    start_date = start.strftime('%s')
    end_date = end.strftime('%s')

    # Basis for requests to EOD API for Intraday price data
    initial_resp = requests.get(f"https://eodhistoricaldata.com/api/intraday/{symbol}.US?api_token={api_key}"
                                f"&from={start_date}"
                                f"&to={end_date}"
                                f"&interval={interval}")

    raw_data = initial_resp.text
    df = pd.read_csv(StringIO(raw_data))
    df["Timestamp"] = df["Timestamp"].apply(lambda x: datetime.datetime.fromtimestamp(x))

    # Test: intraday_data("AAPL", datetime.datetime(2023, 1, 10, 15, 10, 0),
    # datetime.datetime(2023, 1, 10, 16, 0, 0)))

    return df


# Method to request stock prices for a specific period
def close_data(symbol, current_date):

    client = build_connection()
    prices = client.get_prices_eod(symbol,
                                   period="d",
                                   order="a",
                                   from_=current_date,
                                   to=last_day)

    return pd.DataFrame(prices).set_index("date")
