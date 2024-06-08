"""
This module contains the Pairs class to effectively access the data 
and related operations of each Pair that is traded.
"""
import ib_insync
from tws_connection import ib, build_connection 


# Check if a connection exists already
if not ib.isConnected():
    build_connection()

all_data = dict()


class Pair:
    """
    This class should store the data of each stock that is currently traded.
    To reduce overhead, no getter and setter methods were used.
    """

    def __init__(self,
                 tickers: tuple,
                 currency: str):

        # TODO Prüfen ob es sich lohnen würde zwei unterschiedliche currencies zulassen.

        a,b = tickers

        self.tickers: tuple = tickers
        self.ticker_a: str = a
        self.ticker_b: str = b
        self.contract_a: ib_insync.contract.Stock = None
        self.contract_b: ib_insync.contract.Stock = None
        self.quotes_a = None 
        self.quotes_b = None
        self.equation: tuple = None  # (const, slope, threshold)
        self.currency: str = currency
    
    def connect_data(self)
        # Define the contract - TODO make it dependend on the incoming stock - request the data of the stock remotely if possible and
        # fill in the request correctly
        self.contract_a = ib_insync.contract.Stock(pair.ticker_a, "SMART", "USD")
        self.contract_b = ib_insync.contract.Stock(pair.ticker_b, "SMART", "USD")
        # Defining the stock contracts alone is not sufficient. The Stock instances need to be qualified.
        # in order to enable that data can be requested with them.
        ib.qualifyContracts(pair.contract_a)
        data_a = ib.reqMktData(pair.contract_a)
        ib.qualifyContracts(pair.contract_b)
        data_b = ib.reqMktData(pair.contract_b)
        pair.quotes_a = data_a  # TODO Does this make sense or can I insert the request directly?
        pair.quotes_b = data_b
        print("----Connected ticker {pair.ticker_a} and {pair.ticker_b} to data source----")

