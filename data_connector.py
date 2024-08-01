"""
This module contains the Pairs class to effectively access the data 
and related operations of each Pair that is traded.
"""
import ib_insync
import asyncio as aio
from tws_connection import ib, build_connection

# Check if a connection exists already
if not ib.isConnected():
    build_connection()

all_data = dict()


class Pair:
    """
    This class should store the data of each stock that is currently traded.
    """

    def __init__(self,
                 tickers: tuple,
                 currency: str
                 equation: tuple):

        # TODO Prüfen ob es sich lohnen würde zwei unterschiedliche currencies zulassen.

        a, b = tickers

        self.tickers: tuple = tickers
        self.ticker_a: str = a
        self.ticker_b: str = b
        self.contract_a: ib_insync.contract.Stock = None
        self.contract_b: ib_insync.contract.Stock = None
        self.quotes_a = None
        self.quotes_b = None
        self.equation: tuple = equation # (const, slope, threshold)
        self.currency: str = currency#

    @staticmethod
    def _collect_data(ticker, currency):
        # Define the contract - TODO make it dependend on the incoming stock - request the data of the stock remotely
        # if possible and fill in the request correctly
        contract = ib_insync.contract.Stock(ticker, "SMART", currency)
        # Defining the stock contracts alone is not sufficient. The Stock instances need to be qualified.
        # in order to enable that data can be requested with them.
        ib.qualifyContracts(contract)
        data = ib.reqMktData(contract)
        return data, contract

    def connect_data(self):
        data_a, contract_a = self._collect_data(self.ticker_a, self.currency)
        data_b, contract_b = self._collect_data(self.ticker_b, self.currency)
        self.quotes_a = data_a
        self.quotes_b = data_b
        self.contract_a = contract_a
        self.contract_b = contract_b

    def export(self):
        return self.tickers, self.currency
