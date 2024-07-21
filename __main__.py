from data_connector import Pair
from itertools import chain, combinations
from tws_connection import ib, build_connection
import asyncio as aio
import execution_model as em
import ib_insync
import math
import copy

# Check if a connection exists already
if not ib.isConnected():
    build_connection()


def connect_pairs(pairs_traded: list):
    # NOTE Comment this out for real time data.
    ib.reqMarketDataType(3)
    # Transform the tickers into instances of the ib_insync Stock-class (Stock "Contracts").
    for pair in pairs_traded:
        pair.connect_data()


if __name__ == "__main__":
    # Test data
    test_pairs = [Pair(("AAPL", "MSFT"), "USD"),
                  Pair(("GM", "TSLA"), "USD"),
                  Pair(("AMZN", "CPNG"), "USD")]

    connect_pairs(test_pairs)

else:
    raise ImportError("This module is not for external use. This is just a prototype.")
