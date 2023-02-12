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

    def equities_data(stock_ticker):

        ask = []
        bid = []
        timestamp = []

        # Connect to WebSocket API and subscribe to trade feed for a stock symbol
        ws = create_connection(f"wss://ws.eodhistoricaldata.com/ws/us-quote?api_token={api_key}")
        ws.send(f'{{"action": "subscribe", "symbols": "{stock_ticker}"}}')

        # Collecting the first data points
        while len(ask) < 1:
            first_answer = ws.recv()
            first_quote = json.loads(first_answer)
            if len(first_quote) > 2:
                ask.append(first_quote['p'])
                bid.append(first_quote['bp'])
                timestamp.append(datetime.datetime.fromtimestamp(first_quote["t"]/1000.0))

        # Collecting initial data for the real_time_data function
        while True:
            # Number of data points collected - should be as high as tolerable
            # len(ask) < 50 must be equal to len(df["Ask"]) > 50 in the real_time_data.equity_prices function
            if len(ask) < 50:
                result = ws.recv()
                result = json.loads(result)
                if ask[-1] != result['ap']:
                    ask.append(result["ap"])
                    bid.append(result["bp"])
                    timestamp.append(datetime.datetime.fromtimestamp(result["t"]/1000.0))
                    time.sleep(1)
            else:
                equity_prices = pd.DataFrame({"Ask": ask, "Bid": bid, "Time": timestamp})
                ask.clear()
                bid.clear()
                timestamp.clear()
                equity_prices.index = equity_prices["Time"]
                del equity_prices["Time"]
                return equity_prices

    def currencies_data(crypto_pair):

        price = []
        timestamp = []

        # Connect to WebSocket API and subscribe to trade feed for a currency pair symbol
        ws = create_connection(f"wss://ws.eodhistoricaldata.com/ws/crypto?api_token={api_key}")
        ws.send(f'{{"action": "subscribe", "symbols": "{crypto_pair}"}}')

        # Collecting the first data points
        while len(price) < 1:
            first_answer = ws.recv()
            first_quote = json.loads(first_answer)
            if len(first_quote) > 2:
                price.append(first_quote['p'])
                timestamp.append(datetime.datetime.fromtimestamp(first_quote["t"] / 1000.0))

        # Collecting initial data for the real_time_data function
        while True:
            # Number of data points collected - should be as high as tolerable
            # len(price) < 50 must be equal to len(df["Price"]) > 50 in the real_time_data.crypto_pair function
            if len(price) < 10:
                result = ws.recv()
                result = json.loads(result)
                if price[-1] != result['p']:
                    price.append(result['p'])
                    timestamp.append(datetime.datetime.fromtimestamp(result["t"] / 1000.0))
                    time.sleep(1)
            else:
                print(len(price), len(timestamp))
                crypto_frame = pd.DataFrame(
                    {"Price": price, "Time": timestamp})
                price.clear()
                timestamp.clear()
                crypto_frame.index = crypto_frame["Time"]
                del crypto_frame["Time"]
                return crypto_frame

    # Deciding between Cryptocurrency and equity prices
    if '-' in symbol:
        return currencies_data(symbol)
    else:
        return equities_data(symbol)


def real_time_data(symbol):
    def crypto_pair(current_pair):

        # Connect to WebSocket API and subscribe to trade feed for crypto pairs
        ws = create_connection(f"wss://ws.eodhistoricaldata.com/ws/crypto?api_token={api_key}")
        ws.send(f'{{"action": "subscribe", "symbols": "{current_pair}"}}')

        df = collecting_initial_datapoints(current_pair).copy()

        # collecting additional data points for the symbol given
        while True:
            result = ws.recv()
            result = json.loads(result)
            if len(result) > 2:
                while True:
                    result = ws.recv()
                    result = json.loads(result)
                    if df.tail(1).values[0][0] != result['p']:
                        price = result["p"]
                        timestamp = datetime.datetime.fromtimestamp(result["t"] / 1000.0)
                        df.loc[timestamp] = [price]
                        # If maximum number of rows are exceeded by one, one old datapoint will be deleted
                        if len(df["Price"]) > 10:
                            df.drop(index=df.index[0], axis=0, inplace=True)
                        # Getting the trend by running a regression on the rolling datapoints
                        reg_output = stats.linregress(range(len(df["Price"])), df["Price"].astype(float))
                        print(reg_output.slope)  # modification needed - data should be stored in a database
                    time.sleep(1)

    def equity_prices(current_ticker):

        # Connect to WebSocket API and subscribe to trade feed for crypto pairs
        ws = create_connection(f"wss://ws.eodhistoricaldata.com/ws/us-quote?api_token={api_key}")
        ws.send(f'{{"action": "subscribe", "symbols": "{current_ticker}"}}')

        df = collecting_initial_datapoints(current_ticker).copy()

        # collecting additional data points for the symbol given
        while True:
            result = ws.recv()
            result = json.loads(result)
            if len(result) > 2:
                while True:
                    result = ws.recv()
                    result = json.loads(result)
                    if df['Ask'].tail(1) != result["ap"] and df['Bid'].tail(1) != result["bp"]:
                        ask = result["ap"]
                        bid = result["bp"]
                        timestamp = datetime.datetime.fromtimestamp(result["t"] / 1000.0)
                        df.loc[timestamp] = [ask, bid]
                        # If maximum number of rows are exceeded by one, one old datapoint will be deleted
                        if len(df["Ask"]) > 10:
                            df.drop(index=df.index[0], axis=0, inplace=True)
                        # Getting the trend by running a regression on the rolling datapoints
                        reg_output = stats.linregress(range(len(df["Ask"])), df["Ask"].astype(float))
                        print(reg_output.slope)  # modification needed - data should be stored in a database
                    time.sleep(1)

    # Deciding between Cryptocurrency and equity prices
    if '-' in symbol:
        print('Currency detected')
        crypto_pair(symbol)
    else:
        print('Stock Ticker detected')
        equity_prices(symbol)


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
