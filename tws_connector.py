from ib_insync import IB, LimitOrder, MarketOrder


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
