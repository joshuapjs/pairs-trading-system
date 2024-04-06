"""
This module contains the relevant functions to size the current positions that should be taken,
according to the alpha_model properly.
"""
import polygon
import os
import pandas as pd
from data_connector import Pair


def determine_position_size(symbols: list):
    """
    This determines the proper position sizes for a given list of stock symbols
    :param symbols: List of stock symbols
    :return:
    """
    # Instantiate the StockClient
    api_key: str = os.getenv("API_Polygon")
    client = polygon.StocksClient(api_key)

    # Define the empty output DataFrame
    all_prices: dict = dict()

    # Retrieve the price data for each stock in symbols
    for symbol in symbols:
        # Request the data from Polygon.io
        close_price: dict = client.get_snapshot(symbol)["ticker"]["day"]["vw"]
        # Get the close price in a time series
        all_prices[symbol] = close_price

    return all_prices


print(determine_position_size(["AAPL", "MSFT", "TSLA", "CPNG"]))
