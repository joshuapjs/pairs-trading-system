import polars
import pandas as pd
import numpy as np
import ib_insync


class Pair:
    """
    This class should store the data of each stock that is currently traded.
    """

    def __init__(self,
                 pair_traded: tuple,
                 currency: str)

        # TODO Prüfen ob es sich lohnen würde zwei unterschiedliche currencies zulassen.

        first_symbol, second_symbol = pair_traded

        self.symbols = (ticker_a.localSymbol, ticker_b.localSymbol)
        self.first_symbol = first_symbol
        self.second_symbol = second_symbol
        self.first_quote = None
        self.second_quote = None
        self.currency = currency
        self.first_client = None
        self.second_client = None
    
    def get_symbols(self):
        return self.symbols

    def get_currency(self):
        return self.last_quote

    def get_first_ticker(self):
        return self.first_symbol

    def get_second_ticker(self):
        return self.second_symbol

    def _connect_to_ticker(quote_symbol: str):
        """
        This function connects to TWS and builds a connection to a stock ticker symbol.

        quote_symbol: Ticker symbol of the given stock.
        """
        # Setup of the client to request data from TWS

        ib_insync.util.startLoop()
        ib = ib_insync.IB()

        # Connect to local host
        ib.connect("127.0.0.1", 7496, clientId=15)

        # Prepare connection to websocket for quote_symbol
        current_stock = ib_insync.Stock(quote_symbol)
        # Request Bid/Ask quotes from TWS
        ticker = ib.reqTickByTickData(current_stock, 'BidAsk')
        
        # wait for response
        ib.sleep(2)

        # Feedback if connection was built successful. 
        if ticker:
            print(f"Connection to {quote_symbol} established.")
        
        return ib, ticker

    def connect():
        if not self.first_client:
            print(f"Connecting to ticker {self.first_ticker}")
            self.first_client = self._connect_to_ticker(self.first_client)
        elif not self.second_client:
            print(f"Connecting to ticker {self.second_ticker}")
            self.second_client = self._connect_to_ticker(self.second_client)

    def set_first_quote(self, latest_quote):
        self.first_quote = latest_quote 
        print(f"last_quote of {self.first_symbol} was updated.") 
        return 1

    def set_second_quote(self, latest_quote):
        self.second_quote = latest_quote
        print(f"last_quote of {self.second_symbol} was updated.") 
        return 1

    def disconnect_from_ticker(ticker_subscription: tuple):
       # TODO Add this to the destructor of the class.
       ib, current_ticker = ticker_subscription
       ib.cancelTickByTickData(current_ticker.contract, 'BidAsk')

       print(f"Connection to {current_ticker.localSymbol} disconnected")

