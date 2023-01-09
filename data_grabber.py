from websocket import create_connection
import time
import json
import os

api_key = os.environ["API_EOD"]

# Connect to WebSocket API and subscribe to trade feed for Ethereum and Bitcoin - will be replaced by stock prices
ws = create_connection(f"ws://ws.eodhistoricaldata.com/ws/crypto?api_token={api_key}")
ws.send('{"action": "subscribe", "symbols": "ETH-USD"}')

# Infinite loop waiting for WebSocket data
while True:
    result = ws.recv()
    result = json.loads(result)
    print(result)
    time.sleep(1)