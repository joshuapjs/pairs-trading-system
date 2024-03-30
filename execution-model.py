"""
Execution Model
---------------

This Module contains the functions necessary to size and place orders on behalf of the Alpha Model. 
"""

import ib_insync
# util.startLoop()  # uncomment this line when in a notebook

def build_connection():
    """
    A library to build a connection to localhost.
    """
    ib = ib_insync.IB()
    ib.connect('127.0.0.1', 7497, clientId=1)


def place_order(ticker_symbol: str, exchange_mic: str, currency: str, action: str, quantity: str:w):
    """
    This Function places an order for a stock and manages its execution.
    """
    
    # Instantiating the Stock contract.
    current_stock = ib_insync.Stock(symbol=ticker_symbol, 
                                    exchange=exchange_mic, 
                                    currency=currency)
 
    order = ib_insync.LimitOrder(action, quantity)
