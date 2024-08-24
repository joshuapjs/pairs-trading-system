"""
This Module contains the functions that are need to determine if a 
trading opportunity based on the strategy is present.
"""
import ib_insync
import copy
import math
import data_connector as dc
from tws_connection import ib, build_connection

# Check if a connection exists already
if not ib.isConnected():
    build_connection()


def generate_signals(pairs):  # Pairs trading logic ist the Research based insight about selected pairs
    # Hier muss ein Threshold berechnet werden. Wo befinden wir uns,
    # bei Betrachtung der stationären Zeitreihe die Divergenz der Returns darstellt?
    new_signals = {}
    pairs_traded = {}

    for pair in pairs:
        const, slope, threshold = pair.equation
        estimate = const + slope * pair.quotes_b.dict()["ask"]  # TODO Datenzugriff ist ungetestet
        delta = pair.quotes_a.dict()["ask"] - estimate
        if abs(delta) > threshold:
            # assign priority based on strength of deviation
            # TODO find a better way, maybe in terms of the distribution of the variable
            deviation = (delta - threshold) / threshold
            sign = math.copysign(1, delta)
            ticker_a, ticker_b = pair.tickers
            pairs_traded[ticker_a] = pair
            pairs_traded[ticker_b] = pair  # This is memory-wise very inefficient but memory should not be a problem.
            new_signals[pair.tickers] = (deviation,
                                         sign,
                                         pair,
                                         {
                                             ticker_a: copy.copy(pair.quotes_a),
                                             ticker_b: copy.copy(pair.quotes_b)
                                         },
                                         const,
                                         slope,
                                         threshold)
    return new_signals, pairs_traded

