"""
This Module contains the functions that are need to determine if a 
trading opportunity based on the strategy is present.
"""
import ib_insync as ib
import copy
import math
import data_connector as dc


# Check if a connection exists already
if not ib.isConnected():
    build_connection()


def check_for_entry(pair):  # Pairs trading logic ist the Research based insight about selected pairs
    # Hier muss ein Threshold berechnet werden. Wo befinden wir uns,
    # bei Betrachtung der stationären Zeitreihe die Divergenz der Returns darstellt?

    new_signals = {}
    const, slope, threshold = pair.equation
    estimate = const + slope * pair.quotes_b.dict()["ask"]  # TODO Datenzugriff ist ungetestet
    delta = pair.quotes_a.dict()["ask"] - estimate
    if abs(delta) > threshold:
        # assign priority based on strength of deviation
        # TODO find a better way, maybe in terms of the distribution of the variable
        deviation = (delta - threshold) / threshold
        sign = math.copysign(1, delta)
        new_signals[current_pairs.tickers] = (deviation,
                                              sign,
                                              pair,
                                              copy.copy(pair.quote_a),
                                              copy.copy(pair.quote_b),
                                              const,
                                              slope)
        # Das Portfolio Model muss dann basierend auf der stärke der Abweichung und der Richtung,
        # Entscheidungen treffen was gekauft werden soll.
        
    return new_signals

