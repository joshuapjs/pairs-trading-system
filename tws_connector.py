from ib_insync import *


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=2)


def forex_market_order(pair: str, action: str, amount: int):
    eur_usd_contract = Forex(pair, 'IDEALPRO')
    eur_usd_contract_order = MarketOrder(action, amount)
    trade = ib.placeOrder(eur_usd_contract, eur_usd_contract_order)
    return print(trade.log, trade.orderStatus.status)

forex_market_order('EURUSD', 'BUY', 100000)