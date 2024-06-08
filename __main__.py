from data_connector import Pair
from itertools import chain, combinations
from tws_connection import ib, build_connection
import execution_model as em
import ib_insync
import math
import copy


# Check if a connection exists already
if not ib.isConnected():
    build_connection()


def connect_pairs(pairs_traded: list):

    # NOTE Comment this out for real time data. 
    ib.reqMarketDataType(3) 
    ib.sleep(1)

    # Transform the tickers into instances of the ib_insync Stock-class (Stock "Contracts").
    for pair in pairs_traded:
        pair.connect_data()
        ib.sleep(1)


if __name__ == "__main__":
    # Just a quick functionality test
    winning_pairs = [
            Pair(("META", "MSFT"), "USD"),
            Pair(("NVDA", "TSLA"), "USD")
            ]
    pairs = get_stock_data(winning_pairs)

    contract = ib_insync.contract.Stock("TSLA", "SMART", "USD")
    ib.qualifyContracts(contract)
    em.stock_market_order(contract, quantity=1000)
    open_orders = ib.openOrders()
    print(open_orders[0].orderId)
    em.cancel_order(open_orders[0])

else:
    raise ImportError("This module is not for external use. This is just a prototype.")

