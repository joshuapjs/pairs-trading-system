import ib_insync
from itertools import chain, combinations

ib_insync.util.startLoop()
# TODO: Bei Modularisierung muss ib bei den Funktionen als Parameter mitgegeben werden.
ib = ib_insync.IB()

# Connect to TWS.
connection = ib.connect("127.0.0.1", 7497, clientId=15)


def get_stock_data(current_pairs: list):
    recent_asks = dict()

    # NOTE Comment this out for real time data. 
    ib.reqMarketDataType(3) 
    ib.sleep(1)

    # Transform the tickers into instances of the ib_insync Stock-class (Stock "Contracts").
    contracts = [ib_insync.contract.Stock(current_ticker, "SMART", "USD") for current_ticker in list(current_pairs)]

    # Defining the stock contracts alone is not sufficient. The Stock instances need to be qualified.
    # in order to enable that data can be requested with them.
    for current_contract in contracts:
        ib.qualifyContracts(current_contract)
        data = ib.reqMktData(current_contract)
        ib.sleep(1)
        recent_ask[current_contract.symbol] = data.dict()["ask"] 

    return recent_asks


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


def compare_pairs(current_stock_data):
    ticker_symbols = []
    for current_stock in current_stock_data:
        ticker_symbols.append(current_stock.symbol)

    current_signals = dict()

    def powerset(iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    pairs_to_check = list(set([pair for pair in powerset(ticker_symbols) if len(pair) == 2]))

    for stocka, stockb in pairs_to_check:
        if stocka > stockb:
            current_signals[stocka] = 0
            current_singals[stockb] = 1


if __name__ == "__main__":
    ticker_pair = ["AAPL", "TSLA"]
    prices = get_stock_data(ticker_pair)
    
    for ticker in ticker_pair:
        limit_order(limit_price[ticker], stock=ticker)
else:
    raise ImportError("This module is not for external use. This is just a prototype.")

