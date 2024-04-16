import ib_insync
import data_connector as dc

def generate_signal(traded_pair: dc.Pair, threshold: float) -> list(tuple):
    """
    This function generates a signal for each given pair under a specific threshold. The output is a list of tuples, containing the data.

    traded_pair: A dc.Pair obeject of the pair that is evaluated
    threshold: The threshold given under which the Pair is evaluated.
    """
    delta = traded_pair.first_quote - alpha - beta * traded_pair.second_quote  # TODO Model parameter ergänzen

    if threshold <= delta:
        # 11 = BUY; 10 = Hold; 00 = SELL 
        signal = [(traded_pair.second_symbol, 11), 
                  (traded_pair.first_symbol, 00)]

    return signal
