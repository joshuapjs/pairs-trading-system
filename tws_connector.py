from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=0)


def forex_market_order(pair: str, action: str, amount: int):
    eur_usd_contract = Forex(pair, 'IDEALPRO')
    eur_usd_contract_order = MarketOrder(action, amount)
    trade = ib.placeOrder(eur_usd_contract, eur_usd_contract_order)
    ib.sleep(1)
    assert trade in ib.trades()
    return trade.log, trade.orderStatus.status
