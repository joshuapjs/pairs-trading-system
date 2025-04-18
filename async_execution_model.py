"""
This Module contains the functions necessary to size and place orders on behalf of the Alpha Model. 
"""
import copy
import ib_insync
import asyncio as aio
from async_tws_connection import ib, build_connection


async def stock_market_order(contract: ib_insync.contract.Stock, action: str, quantity: int) :
    """
    Wrapper for an ib_insync Market-Order.
    :param contract: The ib_insync.contract.Stock Object, necessary for the exection of the order.
    :param action: Intention to "BUY" or "SELL".
    :param quantity: The quantity of shares to be bought or sold.
    :return:
    """
    order = ib_insync.MarketOrder(action, quantity)
    trade = await ib.placeOrder(contract, order)
    trade.filledEvent += lambda: aio.get_event_loop().create_task(filled_event_handler())


async def filled_event_handler():
    print("Order was filled")
    await aio.sleep(2)

async def main():

    # Check if a connection exists already
    if not ib.isConnected():
        await build_connection()
    contract = ib_insync.contract.Stock("AMZN", "SMART", "USD")
    await ib.qualifyContracts(contract)
    
    # Call the stock_market_order and wait for the cancellation event
    await stock_market_order(contract, "BUY", 100)
    

if __name__ == "__main__":
    ib.run(main())