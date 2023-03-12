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
today = datetime.date.today()
start_short_period = today - datetime.timedelta(days=7)
start_long_period = today - datetime.timedelta(days=200)


# Infinite loop waiting for WebSocket data
def collecting_initial_datapoints(symbol):

    def equities_data(stock_ticker):

        print("Collecting initial data points")

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
            if len(price) < 50:
                result = ws.recv()
                result = json.loads(result)
                if price[-1] != result['p']:
                    price.append(result['p'])
                    timestamp.append(datetime.datetime.fromtimestamp(result["t"] / 1000.0))
                    time.sleep(1)
            else:
                crypto_frame = pd.DataFrame(
                    {"Price": price, "Time": timestamp})
                price.clear()
                timestamp.clear()
                crypto_frame.index = crypto_frame["Time"]
                del crypto_frame["Time"]
                return crypto_frame

    # Deciding between crypto and equity prices
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
                    # Check if received data entails new data
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

    # Deciding between crypto and equity prices
    if '-' in symbol:
        print('Currency detected')
        crypto_pair(symbol)
    else:
        print('Stock Ticker detected')
        equity_prices(symbol)


def stock_intraday(symbol, start, end, interval="1m", stock=False):
    """
    :param symbol: ticker symbol of a currency or US Stock (supported exchanges NYSE or NASDAQ)
    :param start: required format string in ISO 8601 e.g. '2023-01-05T10:00:00'
    :param end: required format string in ISO 8601 e.g. '2023-02-17T23:17:00'
    :param interval: either 1m (standard) or 5m
    :param stock: Must be set as True if data for a stock is requested
    :return: DataFrame
    """

    start_date = datetime.datetime.fromisoformat(start).strftime('%s')
    end_date = datetime.datetime.fromisoformat(end).strftime('%s')

    url = f"https://eodhistoricaldata.com/api/intraday/{symbol}.FOREX?api_token={api_key}" \
          f"&from={start_date}" \
          f"&to={end_date}" \
          f"&interval={interval}"

    if stock:
        url = url.replace('FOREX', 'US')

    # Basis for requests to EOD API for Intraday forex data
    initial_resp = requests.get(url)

    raw_data = initial_resp.text
    df = pd.read_csv(StringIO(raw_data))
    df["Timestamp"] = df["Timestamp"].apply(lambda x: datetime.datetime.fromtimestamp(x))

    return df


def currency_intraday(currency_symbol, start_date, pricing_interval: str):

    def to_epoch(time_stamp):
        epoch_stamp = (pd.Timestamp(time_stamp) - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")
        return epoch_stamp

    client = build_connection()
    exchange_rates = pd.DataFrame(client.get_prices_intraday(currency_symbol + '.FOREX',
                                                             interval=pricing_interval,
                                                             _from=to_epoch(start_date),
                                                             to=to_epoch(today)))

    return exchange_rates


# Method to request stock prices for a specific period
def stock_close_data(symbol, start_date):

    client = build_connection()
    prices = client.get_prices_eod(symbol,
                                   period="d",
                                   order="a",
                                   from_=start_date,
                                   to=today)

    return pd.DataFrame(prices).set_index("date")
