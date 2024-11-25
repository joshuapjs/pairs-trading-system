"""
This module contains the Pairs class to effectively access the data 
and related operations of each Pair that is traded.
"""
import ib_insync
from tws_connection import ib, build_connection
from constants import MARKET_DATA_TYPE

if not ib.isConnected():
    build_connection()

all_data = dict()

class Pair:
    """
    This class stores the data of each stock that is currently traded.

    Each pair that we want to trade is an instance of Pair.
    The Pair class has all necessary data for evaluations about its attractiveness.
    The order of ticker_a and ticker_b does not matter, except for the equation,
    which has to stick to the format

    ticker_a = const + slope * ticker_b

    We can correctly determine under- or overvalutation, independend of the mapping
    as long as the equation is set up correctly.
    """

    def __init__(self,
                 tickers: tuple,
                 currency: str,
                 equation: tuple):
 
        a, b = tickers

        self.tickers: tuple = tickers
        self.ticker_a: str = a
        self.ticker_b: str = b
        self.contract_a: ib_insync.contract.Stock = None
        self.contract_b: ib_insync.contract.Stock = None
        self.quotes_a = None
        self.quotes_b = None
        self.equation: tuple = equation  # (const, slope)
        self.res_vol = float  # This is not used yet but could contain the volatility of the ratio of the prices.
        self.currency: str = currency

    @staticmethod
    def _collect_data(ticker, currency):

        # First we connect the ticker to TWS to receive Market Data.
        # Please change the respective constant in the constants.py file.
        # More information about the different settings: https://ib-insync.readthedocs.io/api.html#ib_insync.ib.IB.reqMarketDataType

        contract = ib_insync.contract.Stock(ticker, "SMART", currency)
        ib.qualifyContracts(contract)
        ib.reqMarketDataType(MARKET_DATA_TYPE)
        data = ib.reqMktData(contract)
        return data, contract

    def connect_data(self):
        data_a, contract_a = self._collect_data(self.ticker_a, self.currency)
        data_b, contract_b = self._collect_data(self.ticker_b, self.currency)
        self.quotes_a = data_a
        self.quotes_b = data_b
        self.contract_a = contract_a
        self.contract_b = contract_b

    def export_essentials(self):
        return self.tickers, self.currency

