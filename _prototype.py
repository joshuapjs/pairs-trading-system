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


def get_stock_data(pairs_traded: list):

    # NOTE Comment this out for real time data. 
    ib.reqMarketDataType(3) 
    ib.sleep(1)

    # Transform the tickers into instances of the ib_insync Stock-class (Stock "Contracts").
    for pair in pairs_traded:
        # Define the contract - TODO make it dependend on the incoming stock - request the data of the stock remotely if possible and
        # fill in the request correctly
        pair.contract_a = ib_insync.contract.Stock(pair.ticker_a, "SMART", "USD")
        pair.contract_b = ib_insync.contract.Stock(pair.ticker_b, "SMART", "USD")
        # Defining the stock contracts alone is not sufficient. The Stock instances need to be qualified.
        # in order to enable that data can be requested with them.
        ib.qualifyContracts(pair.contract_a)
        data_a = ib.reqMktData(pair.contract_a).dict()
        ib.qualifyContracts(pair.contract_b)
        data_b = ib.reqMktData(pair.contract_b).dict()
        ib.sleep(2) # Maybe this is not necessary lets see
        pair.quotes_a = data_a  # TODO Does this make sense of can I insert the request directly?
        pair.quotes_b = data_b

    return pairs_traded


def compare_pairs(current_pairs):  # Pairs trading logic ist the Research based insight about selected pairs
    # Hier muss ein Threshold berechnet werden. Wo befinden wir uns,
    # bei Betrachtung der stationären Zeitreihe die die Divergenz der Returns darstellt ?
    new_signals = dict()
    for pair in current_pairs:
        const, slope, threshold = pair.equation
        estimate = const + slope * pair.quotes_b["ask"]
        delta = pair.quotes_a["ask"] - estimate
        if abs(delta) > threshold:
            # assign priority based on strength of deviation TODO find a better way, maybe in terms of the distribution of the variable
            deviation = (delta - threshold) / threshold
            sign = math.copysign(1, delta)
            new_signals[current_pairs.tickers] = (deviation, sign, pair, (copy.copy(pair.quote_a), copy.copy(pair.quote_b)))
            # Das Portfolio Model muss dann basieredn auf der stärke der Abweichung und der Richtung, Entscheidungen treffen was gekauft werden soll.

    return new_signals


if __name__ == "__main__":
    # Just a quick functionality test
    winning_pairs = [
            Pair(("META", "MSFT"), "USD"),
            Pair(("NVDA", "TSLA"), "USD")
            ]
    pairs = get_stock_data(winning_pairs)
    print(pairs)

    contract = ib_insync.contract.Stock("TSLA", "SMART", "USD")
    ib.qualifyContracts(contract)
    em.stock_market_order(contract, quantity=1000)
    open_orders = ib.openOrders()
    print(open_orders[0].orderId)
    em.cancel_order(open_orders[0])

else:
    raise ImportError("This module is not for external use. This is just a prototype.")

