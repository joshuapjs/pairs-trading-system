import ib_insync
from itertools import chain, combinations

ib_insync.util.startLoop()
# TODO: Bei Modularisierung muss ib bei den Funktionen als Parameter mitgegeben werden.
ib = ib_insync.IB()

# Connect to TWS.
connection = ib.connect("127.0.0.1", 7497, clientId=15)


def get_stock_data(pairs_trading_logic: dict):
    recent_prices = dict()

    # NOTE Comment this out for real time data. 
    ib.reqMarketDataType(3) 
    ib.sleep(1)

    # Transform the tickers into instances of the ib_insync Stock-class (Stock "Contracts").
    contracts = [ib_insync.contract.Stock(ticker_a, "SMART", "USD"), ib_insync.contract.Stock(ticker_b, "SMART", "USD")
                 for ticker_a, ticker_b in pairs_trading_logic.keys()]

    # Defining the stock contracts alone is not sufficient. The Stock instances need to be qualified.
    # in order to enable that data can be requested with them.
    for ticker_a, ticker_b in contracts:
        ib.qualifyContracts(ticker_a)
        data_a = ib.reqMktData(ticker_a)
        ib.qualifyContracts(ticker_b)
        data_b = ib.reqMktData(ticker_b)
        ib.sleep(1)
        recent_prices[ticker_a.symbol] = (data_a.dict()["ask"], data_a.dict()["bid"])
        recent_prices[ticker_b.symbol] = (data_b.dict()["ask"], data_b.dict()["bid"])

    return recent_prices 


def limit_order(limit_price: int, stock: str, exchange: str = "SMART", currency="USD", action="BUY", quantity=1000) :
    # Instantiating the Stock contract.
    contract = ib_insync.Stock(symbol=stock, 
                                    exchange=exchange, 
                                    currency=currency)
 
    order = ib_insync.LimitOrder(action, quantity, limit_price)
    ib.placeOrder(contract, order)
    ib.sleep(1)


def market_order(stock: str, exchange: str = "SMART", currency="USD", action="BUY", quantity=1000) :
    contract = ib_insync.Stock(symbol=stock, 
                                    exchange=exchange, 
                                    currency=currency)
 
    order = ib_insync.MarketOrder(action, quantity)
    ib.placeOrder(contract, order)
    ib.sleep(1)


def compare_pairs(current_prices, pairs_trading_logic):  # Pairs trading logic ist the Research based insight about selected pairs

    current_signals = dict()
    # Hier muss ein Threshold berechnet werden. Wo befinden wir uns,
    # bei Betrachtung der stationären Zeitreihe die die Divergenz der Returns darstellt ? 


if __name__ == "__main__":
    # Just a quick functionality test

    winning_pairs = {("AAPL","TSLA"):(None,None), ("MSFT","NVDA"): (None,None)} 
    prices = get_stock_data(winning_pairs)
    
    for ticker in prices:
        limit_order(limit_price[ticker.symbol], stock=ticker)
else:
    raise ImportError("This module is not for external use. This is just a prototype.")

