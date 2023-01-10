import pandas as pd
from websocket import create_connection
import datetime
import time
import json
import os

api_key = os.environ["API_EOD"]

# Connect to WebSocket API and subscribe to trade feed for Ethereum and Bitcoin - will be replaced by stock prices
ws = create_connection(f"wss://ws.eodhistoricaldata.com/ws/us-quote?api_token={api_key}")
ws.send('{"action": "subscribe", "symbols": "TSLA"}')


# Infinite loop waiting for WebSocket data
def real_time_data():

    ask = []
    bid = []
    timestamp = []

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
            print(prices)
            ask.clear()
            bid.clear()
            timestamp.clear()


real_time_data()
