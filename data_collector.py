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

# Calculating three different dates for defining the relevant lengths of the time series
last_day = datetime.date.today()
start_short_period = last_day - datetime.timedelta(days=7)
start_long_period = last_day - datetime.timedelta(days=200)


# Infinite loop waiting for WebSocket data
def collecting_initial_datapoints(symbol):

    ask = []
    bid = []
    timestamp = []

    # Connect to WebSocket API and subscribe to trade feed for a stock symbol
    ws = create_connection(f"wss://ws.eodhistoricaldata.com/ws/us-quote?api_token={api_key}")
    ws.send(f'{{"action": "subscribe", "symbols": "{symbol}"}}')

    # Collecting the first data points
    while len(ask) < 1:
        first_answer = ws.recv()
        first_quote = json.loads(first_answer)
        if len(first_quote) > 2:
            ask.append(first_quote['ap'])
            bid.append(first_quote['bp'])
            timestamp.append(datetime.datetime.fromtimestamp(first_quote["t"]/1000.0))

    # Collecting initial data for the real_time_data function
    while True:
        # Number of data points collected - should be as high as tolerable
        # len(ask) < 50 must be equal to len(df["Ask"]) > 50 in the real_time_data function
        if len(ask) < 50:
            result = ws.recv()
            result = json.loads(result)
            if ask[-1] != result['ap']:
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
    ws = create_connection(f"wss://ws.eodhistoricaldata.com/ws/us-quote?api_token={api_key}")
    ws.send(f'{{"action": "subscribe", "symbols": "{symbol}"}}')

    df = collecting_initial_datapoints(symbol).copy()

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
                if len(df["Ask"]) > 50:
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
