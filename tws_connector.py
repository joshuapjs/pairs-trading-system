from ib_insync import IB, Forex, Stock, LimitOrder

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=0)


def forex_market_order(pair: str, action: str, amount: int, limit_price: float):
    eur_usd_contract = Forex(pair, 'IDEALPRO')
    eur_usd_contract_order = LimitOrder(action, amount, limit_price)
    trade = ib.placeOrder(eur_usd_contract, eur_usd_contract_order)
    ib.sleep(1)
    assert trade in ib.trades()
    return trade.log, trade.orderStatus.status


def stock_market_order(symbol: str, limit_price: float, action: str, amount: int,
                       currency: str = "EUR", exchange: str = "CBOE"):
    current_stock = Stock(symbol, exchange, currency)
    current_stock_order = LimitOrder(action, amount, limit_price)
    trade = ib.placeOrder(current_stock, current_stock_order)
    ib.sleep(1)
    assert trade in ib.trades()
    return trade.log, trade.orderStatus.status
