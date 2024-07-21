"""
This Module contains the functions necessary to size and place orders on behalf of the Alpha Model. 
"""
import ib_insync
import asyncio as aio
from tws_connection import ib, build_connection


# Check if a connection exists already
if not ib.isConnected():
    build_connection()


def cancel_order(order_to_cancel):
    ib.cancelOrder(order_to_cancel)
    ib.sleep(1)


def stock_limit_order(contract: ib_insync.contract.Stock, limit_price: int, action="BUY", quantity=10):
    order = ib_insync.LimitOrder(action, quantity, limit_price)
    ib.placeOrder(contract, order)
    ib.sleep(1)


def stock_market_order(contract: ib_insync.contract.Stock, action="BUY", quantity=10) :
    order = ib_insync.MarketOrder(action, quantity)
    ib.placeOrder(contract, order)
    ib.sleep(1)

