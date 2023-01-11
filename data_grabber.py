from websocket import create_connection
import pandas as pd
from io import StringIO
import requests
import datetime
import time
import json
import os

api_key = os.environ["API_EOD"]


# Infinite loop waiting for WebSocket data
def real_time_data():

    ask = []
    bid = []
    timestamp = []

    # Connect to WebSocket API and subscribe to trade feed for Ethereum and Bitcoin - will be replaced by stock prices
    ws = create_connection(f"wss://ws.eodhistoricaldata.com/ws/us-quote?api_token={api_key}")
    ws.send('{"action": "subscribe", "symbols": "TSLA"}')

    while True:
        if len(ask) < 5:
            result = ws.recv()
            result = json.loads(result)
            if len(result) > 2:
                ask.append(result["ap"])
                bid.append(result["bp"])
                timestamp.append(datetime.datetime.fromtimestamp(result["t"]/1000.0))
                time.sleep(1)
        else:
            prices = pd.DataFrame({"Ask": ask, "Bid": bid, "Time": timestamp})
            ask.clear()
            bid.clear()
            timestamp.clear()
            return prices


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

    print(initial_resp)
    raw_data = initial_resp.text
    df = pd.read_csv(StringIO(raw_data))
    print(df)


intraday_data("AAPL", datetime.datetime(2022, 1, 10, 15, 10, 0), datetime.datetime(2022, 1, 10, 16, 0, 0))
