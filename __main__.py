from data_connector import Pair
from tws_connection import ib, build_connection
import execution_model
import alpha_model
from constants import ACCOUNT_NUMBER, PAIRS_TRADED, BUDGET
from portfolio_model import Portfolio

# TODO The Executionfunction should try to minimize trading cost. This Calculation should run during the initialization there must be an initialize function, that calculates current relevant measures for the execution model and possibly the Regression.
# TODO implement controls through terminal

# Check if a connection exists already
if not ib.isConnected():
    build_connection()

def connect_pairs(pairs):
    for pair in pairs:
        pair.connect_data()

if __name__ == "__main__":
    portfolio = Portfolio(account_number=ACCOUNT_NUMBER, slots=PAIRS_TRADED, budget=BUDGET)
    # TODO Replace test data with real data.
    test_pairs = [Pair(("AAPL", "MSFT"), "USD", (1,1,1)),
                  Pair(("GM", "TSLA"), "USD", (1,1,1)),
                  Pair(("AMZN", "CPNG"), "USD", (1,1,1))]

    connect_pairs(test_pairs)
    ib.sleep(3)
    
    signals = alpha_model.generate_signals(test_pairs)

    # Erstelle das Initale Portfolio
    initial_execution = portfolio.analyze_signals(signals)
    execution_model.execute_portfolio_adjustments(portfolio, initial_execution)

    while True:
        ib.sleep(10)
        new_adjustments = portfolio.optimize()
        execution_model.execute_portfolio_adjustments(portfolio, new_adjustments)

else:
    raise ImportError("This module is not for external use")

