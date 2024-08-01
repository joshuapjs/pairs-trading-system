from data_connector import Pair
from tws_connection import ib, build_connection
import execution_model
import alpha_model
from portfolio_model import Portfolio

# Check if a connection exists already
if not ib.isConnected():
    build_connection()


def connect_pairs(pairs):
    for pair in pairs:
        pair.connect_data()

if __name__ == "__main__":
    # Create a new Portfolio TODO Log the last Portfolio and load if the existet one in the past.
    portfolio = Portfolio()
    # Test data TODO Equation muss eingefügt werder sobald Test Daten verfügbar sind. (Siehe Alpha Model)
    test_pairs = [Pair(("AAPL", "MSFT"), "USD", (1,1,1)),
                  Pair(("GM", "TSLA"), "USD", (1,1,1)),
                  Pair(("AMZN", "CPNG"), "USD", (1,1,1))]
    
    # Generiere die initialen Signale TODO Sollte nur gemacht werden wenn es kein Portfolio log zum laden gibt.
    signals = alpha_model.generate_signals(test_pairs)

    # Erstelle das Initale Portfolio
    initial_execution = portfolio.analyze_signals(signals)  # TODO Wenn das eine Klasse ist warum return diese Methode ? Ist das gut so ?
    execution_model.execute_portfolio_adjustments(initial_execution)
    # TODO implement controls through terminal
    while True:
        ib.sleep(90)
        new_adjustments = portfolio.optimize()
        execution_model.execute_portfolio_adjustments(new_adjustments)

else:
    raise ImportError("This module is not for external use")

