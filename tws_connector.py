from ib_insync import IB, LimitOrder, MarketOrder, Stock, Forex


def place_order(asset, action: str, amount: int, limit_price: float = None):
    """
    This function will place a limit or market order on IBKR through the TWS.
    :param asset: An instantiated asset class from the ib_insync library
    :param action: "BUY" or "SELL".
    :param amount: Amount of items of the asset.
    :param limit_price: If specified the order will become a limit order, otherwise a
    market order will be placed instead.
    :return: Current trade logbook and the current order status.
    """
    # Connecting to the TWS through the local host.
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)
    # Creating a limit order if the limit order is specified and a market order of the
    # limit order price remains unspecified.
    eur_usd_contract_order = LimitOrder(action, amount, limit_price) \
        if limit_price is not None else MarketOrder(action, amount)
    # Placing the order specified order.
    trade = ib.placeOrder(asset, eur_usd_contract_order)
    # Giving the System time to process the order.
    ib.sleep(1)
    return trade.log, trade.orderStatus.status


def get_current_quotes(symbol: str):
    """
    This function returns a list of the current quotes for a given stock
    :param symbol: current stock symbol
    :return: list of current quotes for the stock
    """
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)
    # Instantiating the Stock class in order to define a Contract object
    current_stock = Forex(symbol)
    ticker = ib.reqMktData(current_stock)
    ib.sleep(1)
    ib.cancelMktData(current_stock)
    # Returning a list of the current quotes
    return ticker.prevBid, ticker.prevAsk

print(get_current_quotes("EURUSD"))