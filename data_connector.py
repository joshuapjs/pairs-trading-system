import polars
import pandas as pd
import numpy as np
import ib_insync


class Pair:
    """
    This class should store the data of each stock that is currently traded.
    To reduce overhead, no getter and setter methods were used.
    """

    def __init__(self,
                 tickers: tuple,
                 currency: str):

        # TODO Prüfen ob es sich lohnen würde zwei unterschiedliche currencies zulassen.

        long_ticker, short_ticker = tickers

        self.tickers = tickers
        self.long_ticker = long_ticker
        self.short_ticker = short_ticker
        self.long_quote = None
        self.short_quote = None
        self.currency = currency
    

class Connection:
    """
    Build a connection to TWS and request data.
    """
    # NOTE: The current_pairs MUST be a dictionary mapping a frozenset containing both tickers on the contract.
    # NOTE: Around the (Price)-Events produced by this class should the whole application be built.
    # Setup of the client to request data from TWS.
    def __init__(self, current_pairs: dict):
        # A list containing the current Pairs that are traded.
        self.current_pairs = current_pairs
        self.current_tickers = set()  # Set that contains all current tickers, data is requested for.
        self.current_stocks = list() # List containing the Stock class instances.

    def connect(self):
        ib_insync.util.startLoop()
        ib = ib_insync.IB()

        # Connect to TWS.
        ib.connect("127.0.0.1", 7497, clientId=15)

        # NOTE Comment this out for real time data. 
        ib.reqMarketDataType(3) 
        
        ib.sleep(3)
        # Unpacking instances of the Pair class.
        for pair in list(self.current_pairs.values()):
                self.current_tickers.add(pair.long_ticker)
                self.current_tickers.add(pair.short_ticker)

        # Transform the tickers into instances of the ib_insync Stock-class (Stock "Contracts").
        contracts = [ib_insync.contract.Stock(current_ticker, "SMART", "USD") for current_ticker in list(self.current_tickers)]
        
        # We safe the contracts just created in a list that can be adjusted.
        self.current_stocks = contracts
        # Defining the stock contracts alone is not sufficient. The Stock instances need to be qualified.
        # in order to enable that data can be requested with them.
        for current_contract in self.current_stocks:
            ib.qualifyContracts(current_contract)
            data = ib.reqMktData(current_contract)
            ib.sleep(1)
            print(data)

        # TODO: The Marketdata requested, has to update each relevant Pair instance. So that there are initial values in it.
        # TODO: Maybe then there should be an almost endless function running (in a separated Procces or as main Process?)
        #       that updates all the Pairs, resulting in a new price event. whenever a suffucient threshhold of such price events
        #       is reached (every price event might be too much?) the calculation should run and trades placed etc.

if __name__ == "__main__":
    ticker_pair = Connection({frozenset(("AAPL", "TSLA")) : Pair(("AAPL", "TSLA"), "EUR")})
    ticker_pair.connect()
